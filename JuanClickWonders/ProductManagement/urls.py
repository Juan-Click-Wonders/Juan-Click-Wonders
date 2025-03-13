from django.urls import path
from ProductManagement.views import ProductListCreateApi, ProductDetailApi, CategoryListCreateApi, CategoryDetailApi

urlpatterns = [
    path("products/", ProductListCreateApi.as_view(), name="product_list"),
    path("products/<int:product_id>", ProductDetailApi.as_view(), name="product_detail"),
    path("category/", CategoryListCreateApi.as_view(), name="category_list"),
    path("category/<int:category_id>", CategoryDetailApi.as_view(), name="category_detail"),
]
