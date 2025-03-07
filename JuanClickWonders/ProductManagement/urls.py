from django.urls import path
from ProductManagement import views

# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path("products/", views.productsApi, name="product_list"),
    path("products/<int:id>", views.productsApi, name="product_detail"),
    path("category/", views.categoryApi, name="category_list"),
    path("category/<int:id>", views.categoryApi, name="category_detail"),
]
