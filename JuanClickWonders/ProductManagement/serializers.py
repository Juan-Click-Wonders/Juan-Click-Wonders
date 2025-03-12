from rest_framework import serializers
from ProductManagement.models import Products, Category


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
