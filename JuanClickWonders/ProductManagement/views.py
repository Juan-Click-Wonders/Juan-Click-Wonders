import requests
from django.conf import settings
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from ProductManagement.models import Products, Category, Cart, CartItem, Payment
from ProductManagement.serializers import ProductsSerializer, CategorySerializer, CartSerializer, CartItemSerializer


class ProductListCreateApi(generics.ListCreateAPIView):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name', 'brand', 'category__category_name']
    ordering_fields = ['product_id', 'price', 'sold_products']

    def get_queryset(self):
        queryset = Products.objects.all()

        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        categories = self.request.query_params.getlist('category')
        if categories:
            queryset = queryset.filter(category__category_name__in=categories)

        brands = self.request.query_params.getlist('brand')
        if brands:
            queryset = queryset.filter(brand__in=brands)

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except (ValueError, TypeError):
                pass

        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except (ValueError, TypeError):
                pass

        return queryset.distinct()


class ProductDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = "product_id"


class CategoryListCreateApi(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "category_id"

# class RatingsCreateView(generics.CreateAPIView):
#     queryset = Ratings.objects.all()
#     serializer_class = RatingsSerializer

# class RatingsListView(generics.ListAPIView):
#     queryset = Ratings.objects.all()
#     serializer_class = RatingsSerializer

# class RatingsDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Ratings.objects.all()
#     serializer_class = RatingsSerializer
#     lookup_field = 'pk'


class CartListCreateApi(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class CartRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user.profile)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if obj.user != request.user.profile:
            raise PermissionDenied(
                "You don't have permission to access this cart")


class CartItemListCreateApi(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_id'])

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.get(cart_id=self.kwargs['cart_id'])
        product_id = request.data.get('product')
        new_quantity = request.data.get('quantity')

        existing_item = CartItem.objects.filter(
            cart=cart, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += int(new_quantity)
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        cart = Cart.objects.get(cart_id=self.kwargs['cart_id'])
        serializer.save(cart=cart)


class CartItemRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_id'])


class ProductStockStatusApi(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({
            'in_stock': instance.stock > 0,
            'available_stock': instance.stock
        })


class PaymentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=self.request.user.profile)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        method = request.data.get('method')
        if method not in ['COD', 'GCS', 'MYA']:
            return Response({"error": "Invalid or missing payment method."}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price *
                           item.quantity for item in cart_items)

        additional_info = None
        action_url = None

        if total_amount <= 0:
            return Response({
                "error": "The cart is empty.",
                "total_amount": total_amount,
                "additional_info": additional_info,
                "action_url": action_url,
            }, status=status.HTTP_400_BAD_REQUEST)

        if method == 'COD':
            payment_successful = True
        elif method == 'GCS' or method == 'MYA':
            xendit_response = self.process_ewallet_payment(
                total_amount, method)
            xendit_response_data = xendit_response.json()

            if "error" in xendit_response_data or "error_code" in xendit_response_data:
                payment_successful = False
                additional_info = xendit_response_data
            else:
                actions = xendit_response_data.get('actions', [])

                for action in actions:
                    if action.get('url_type') == 'WEB':
                        action_url = action.get('url')
                        break

                payment_successful = True
                additional_info = xendit_response_data
        else:
            payment_successful = False

        Payment.objects.create(
            user=self.request.user.profile,
            cart=cart,
            method=method,
            amount=total_amount,
            success=payment_successful
        )

        if payment_successful:
            cart_items.delete()
            return Response({
                "message": f"Payment is now being processed via {method}.",
                "total_amount": total_amount,
                "additional_info": additional_info,
                "action_url": action_url,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Payment failed.",
                "additional_info": additional_info
            }, status=status.HTTP_400_BAD_REQUEST)

    def process_ewallet_payment(self, amount, method):
        try:
            channel_code = "GCASH" if method == 'GCS' else "PAYMAYA"
            xendit_response = requests.post(
                url="https://api.xendit.co/payment_requests",
                json={
                    "amount": amount,
                    "currency": "PHP",
                    "country": "PH",
                    "payment_method": {
                        "type": "EWALLET",
                        "ewallet": {
                            "channel_code": channel_code,
                            "channel_properties": {
                                # Replace these placeholders with their corresponding frontend urls
                                "success_return_url": "https://redirect.me/goodstuff",
                                "failure_return_url": "https://redirect.me/badstuff",
                                "cancel_return_url": "https://redirect.me/cancelstuff"
                            }
                        },
                        "reusability": "ONE_TIME_USE"
                    }
                },
                headers={
                    "Authorization": f"Basic {settings.XENDIT_SECRET_KEY}"
                },
                timeout=30
            )

            return xendit_response

        except requests.RequestException as e:
            raise RuntimeError(f"E-Wallet payment request failed: {e}")
