from rest_framework import serializers
from ProductManagement.models import Products, Category, Cart, CartItem, Rating, Order


class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.category_name", read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
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
            "category",
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
    
class RatingSerializer(serializers.ModelSerializer):
    # Add a field that will accept either a string URL or a file upload
    class Meta:
        model = Rating
        fields = ['id', 'product', 'user', 'rating', 'description', 'created_at', 'image_url', 'user_name']
        extra_kwargs = {
            'image_url': {'required': False},
            'user_name': {'required': False}
        }

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
        
    def to_representation(self, instance):
        """Convert the image URL to an absolute URL in the output and ensure user_name is populated"""
        ret = super().to_representation(instance)
        request = self.context.get("request")
        
        # Handle image URL
        if request and instance.image_url:
            ret['image_url'] = request.build_absolute_uri(instance.image_url.url)
        
        # Ensure user_name is populated
        if not ret.get('user_name') and instance.user:
            # Try to get the user's name from various possible sources
            user_profile = instance.user
            user = getattr(user_profile, 'user', None)
            
            if user_profile and hasattr(user_profile, 'first_name') and user_profile.first_name:
                ret['user_name'] = user_profile.first_name
            elif user and hasattr(user, 'first_name') and user.first_name:
                ret['user_name'] = user.first_name
            elif user and hasattr(user, 'username'):
                ret['user_name'] = user.username
            else:
                # Default to first letter of related username or 'User'
                ret['user_name'] = getattr(user, 'username', 'User')
        
        return ret
    

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'product', 'quantity', 'status', 'user']

    def get_product(self, obj):
        if obj.product:
            return {
                "name": obj.product.name,
                "price": obj.product.price
            }
        return None
    
    def get_status(self, obj):
        return obj.get_status_display()