from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from .models import Cart, CartItem, Products
from .serializers import CartSerializer, CartItemSerializer, ProductsSerializer
from ProductManagement.models import Category
from ProductManagement.serializers import CategorySerializer


class ProductListCreateApi(generics.ListCreateAPIView):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = ['name', 'brand', 'category__category_name'] 
    ordering_fields = ['product_id', 'price', 'sold_products']

    def get_queryset(self):
        queryset = Products.objects.all()
        
        # Get search terms for name search
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Handle multiple categories
        categories = self.request.query_params.getlist('category')
        if categories:
            queryset = queryset.filter(category__category_name__in=categories)

        # Handle multiple brands
        brands = self.request.query_params.getlist('brand')
        if brands:
            queryset = queryset.filter(brand__in=brands)

        # Handle price range
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




class ProductCreateView(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'pk'  # This will look up the product by its primary key (id)

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'pk'

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'pk'

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

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer  

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

class CategoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

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
            raise PermissionDenied("You don't have permission to access this cart")

class CartItemListCreateApi(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_id'])

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.get(cart_id=self.kwargs['cart_id'])
        product_id = request.data.get('product')
        new_quantity = request.data.get('quantity')

        existing_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
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
      
@csrf_exempt
def productsApi(request, id=0):
    if request.method == "GET":
        if id != 0:
            product = Products.objects.filter(product_id=id).first()
            if product:
                product_serializer = ProductsSerializer(
                    product, context={"request": request}
                )
                return JsonResponse(product_serializer.data, safe=False)
            return JsonResponse({"error": "Product not found"}, status=404)
        products = Products.objects.all()

        if not products.exists():
            return JsonResponse({"message": "No items in products"}, status=200)

        products_serializer = ProductsSerializer(
            products, many=True, context={"request": request}
        )
        return JsonResponse(products_serializer.data, safe=False)

    elif request.method == "POST":
        products_data = request.POST.dict()
        image_url = request.FILES.get("image_url")

        if not image_url:
            return JsonResponse({"error": "No image submitted."}, status=400)

        products_data["image_url"] = image_url

        category_id = products_data.get("category")

        if not category_id:
            return JsonResponse({"error": "Category ID is required"}, status=400)

        category = Category.objects.filter(category_ID=int(category_id)).first()

        if not category:
            return JsonResponse({"error": "Invalid category ID"}, status=400)

        products_serializer = ProductsSerializer(
            data=products_data, context={"request": request}
        )

        if products_serializer.is_valid():
            product = products_serializer.save(category=category)
            product.image_url = image_url
            product.save()
            return JsonResponse({"message": "Added Successfully"}, safe=False)

        return JsonResponse({"error": products_serializer.errors}, status=400)

    elif request.method == "PUT":
        products_data = request.POST.dict()
        product_id = products_data.get("product_ID")

        if not product_id:
            return JsonResponse({"error": "product_ID is required"}, status=400)

        product = Products.objects.filter(product_ID=product_id).first()
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)

        product_serializer = ProductsSerializer(product, data=products_data)
        if product_serializer.is_valid():
            product = product_serializer.save()

            if "image_url" in request.FILES:
                product.image_url = request.FILES["image_url"]
                product.save()

            return JsonResponse({"message": "Updated Successfully"}, status=200)

        return JsonResponse({"error": product_serializer.errors}, status=400)

    elif request.method == "DELETE":
        product = Products.objects.filter(product_id=id).first()
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)

        product.delete()
        return JsonResponse({"message": "Deleted Successfully"}, status=200)


@csrf_exempt
def categoryApi(request, id=0):
    if request.method == "GET":
        if id != 0:
            category = Products.objects.filter(category_ID=id).first()
            if category:
                category_serializer = CategorySerializer(category)
                return JsonResponse(category_serializer.data, safe=False)
            return JsonResponse({"Error!": "Product not found"}, status=404)
        category = Category.objects.all()

        if not category.exists():
            return JsonResponse({"message": "No existing categories"}, status=200)

        category_serializer = CategorySerializer(category, many=True)
        return JsonResponse(category_serializer.data, safe=False)

    elif request.method == "POST":
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Error! Failed to Add", safe=False)

    elif request.method == "PUT":
        category_data = JSONParser().parse(request)
        category = category.objects.get(category_ID=category_data["category_ID"])
        category_serializer = CategorySerializer(category, data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Error! Failed to Update")

    elif request.method == "DELETE":
        category = category.objects.get(category_ID=id)
        category.delete()
        return JsonResponse("Deleted Successfully", safe=False)
