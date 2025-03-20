from rest_framework import serializers
from ProductManagement.models import Products, Category, Cart, CartItem


class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.category_name", read_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = [
            "product_id",
            "name",
            "description",
            "brand",
            "price",
            "stock",
            "sold_products",
            "image_url",
            "category_name",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image_url:
            return request.build_absolute_uri(f"/media/product_images/{obj.image_url}")
        return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']
        read_only_fields = ['cart']  # Make cart read-only since we set it in the view

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        
        # Get the product instance
        product = None
        if self.instance:
            product = self.instance.product
        elif 'product' in self.initial_data:
            product_id = self.initial_data.get('product')
            try:
                product = Products.objects.get(pk=product_id)
            except Products.DoesNotExist:
                raise serializers.ValidationError("Invalid product")
            
        if product and value > product.stock:
            raise serializers.ValidationError(f"Only {product.stock} items available in stock")
            
        return value

    def validate(self, data):
        # Remove cart validation since it's handled in the view
        return data

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "cart_id", 
            "user", 
            "updated_at", 
            "cart_items", 
            "total_items", 
            "total_price"
        ]

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.cart_items.all())

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.cart_items.all())
