import requests
from django.conf import settings
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from urllib.parse import quote

from ProductManagement.models import Products, Category, Cart, CartItem, Payment, Rating, Wishlist
from ProductManagement.serializers import ProductsSerializer, CategorySerializer, CartSerializer, CartItemSerializer, RatingSerializer


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


class RatingsCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        # Debug incoming request data
        print("Request Data Type:", type(request.data))
        print("Request Data:", request.data)
        print("Request FILES:", request.FILES)

        # Handle the file upload explicitly
        data = request.data.copy()

        # Check if file exists in request.FILES
        if 'image_url' in request.FILES:
            print("Image found in request.FILES with key 'image_url'")
            data['image_url'] = request.FILES['image_url']
        elif 'image' in request.FILES:
            print("Image found in request.FILES with key 'image'")
            # Rename 'image' to 'image_url' to match our model field
            data['image_url'] = request.FILES['image']

        # Create a serializer with our modified data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        if Rating.objects.filter(user=self.request.user.profile, product_id=product_id).exists():
            raise PermissionDenied("You have already rated this product")

        # Get the user's name from the profile or user object
        user_name = None
        if hasattr(self.request.user, 'first_name') and self.request.user.first_name:
            user_name = self.request.user.first_name
        elif hasattr(self.request.user.profile, 'first_name') and self.request.user.profile.first_name:
            user_name = self.request.user.profile.first_name
        elif hasattr(self.request.user, 'username'):
            user_name = self.request.user.username

        # If user_name was provided in the request, use it instead (for frontend compatibility)
        if 'user_name' in self.request.data:
            user_name = self.request.data.get('user_name')

        serializer.save(user=self.request.user.profile, user_name=user_name)


class RatingsListView(generics.ListAPIView):
    serializer_class = RatingSerializer

    def get_permissions(self):
        # Allow anonymous users to view ratings, but require auth for user-specific queries
        if self.request.query_params.get('user_ratings'):
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        queryset = Rating.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if self.request.query_params.get('user_ratings'):
            if self.request.user.is_authenticated:
                queryset = queryset.filter(user=self.request.user.profile)
            else:
                queryset = Rating.objects.none()  # Return empty queryset for unauthenticated users
        return queryset


class RatingsDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def check_object_permissions(self, request, obj):
        if obj.user != request.user.profile:
            raise PermissionDenied("You can only modify your own ratings")
        super().check_object_permissions(request, obj)


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
        channel_code = "GCASH" if method == 'GCS' else "PAYMAYA"
        paymentError = quote("The payment was unsuccessful. Please try again")
        try:
            return requests.post(
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
                                "success_return_url": "http://localhost:5173/orders",
                                "failure_return_url": f"http://localhost:5173/cart?paymentError={paymentError}",
                                "cancel_return_url": f"http://localhost:5173/cart?paymentError={paymentError}"
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

        except requests.RequestException as e:
            raise RuntimeError(f"E-Wallet payment request failed: {e}")


class WishlistAddAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        if not product_id:
            return Response(
                {"error": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        user_profile = self.request.user.profile
        if product in user_profile.wishlist.products.all():
            return Response(
                {'message': 'Product already in wishlist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user_profile.wishlist.products.add(product)
            user_profile.wishlist.save()
            return Response(
                {"message": "Product added to wishlist."},
                status=status.HTTP_200_OK
            )


class WishlistRemoveAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        if not product_id:
            return Response(
                {"error": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        user_profile = self.request.user.profile
        if product not in user_profile.wishlist.products.all():
            return Response(
                {'message': 'Product not in wishlist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user_profile.wishlist.products.remove(product)
            user_profile.wishlist.save()
            return Response(
                {"message": "Product removed from wishlist."},
                status=status.HTTP_200_OK
            )


class WishlistRetrieveAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = self.request.user.profile
        
        # Ensure the user has a wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
        
        products = wishlist.products.all()
        
        # Return a list of product IDs and their details
        result = []
        for product in products:
            result.append({
                "id": f"wishlist_{product.product_id}",  # Using a unique ID format for frontend
                "product": product.product_id
            })
            
        return Response(
            result,
            status=status.HTTP_200_OK
        )


class WishlistToggleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        if not product_id:
            return Response(
                {"detail": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        user_profile = self.request.user.profile
        
        # Ensure the user has a wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=user_profile)
        
        # Check if product is already in wishlist
        is_in_wishlist = product in wishlist.products.all()
        
        if is_in_wishlist:
            # Remove product from wishlist
            wishlist.products.remove(product)
            action = "removed from"
        else:
            # Add product to wishlist
            wishlist.products.add(product)
            action = "added to"
        
        wishlist.save()
        
        return Response(
            {
                "message": f"Product {action} wishlist.",
                "is_in_wishlist": not is_in_wishlist
            },
            status=status.HTTP_200_OK
        )
