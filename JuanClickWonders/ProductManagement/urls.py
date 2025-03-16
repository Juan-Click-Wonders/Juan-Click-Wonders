from django.urls import path
from ProductManagement import views
from ProductManagement.views import (
    CartItemListCreateApi, 
    CartItemRetrieveUpdateDestroyApi, 
    CartListCreateApi, 
    CartRetrieveUpdateDestroyApi,
    ProductStockStatusApi,
    productsApi, 
    categoryApi
)

urlpatterns = [
    path("products/", views.productsApi, name="product_list"),
    path("products/<int:id>", views.productsApi, name="product_detail"),
    path("category/", views.categoryApi, name="category_list"),
    path("category/<int:id>", views.categoryApi, name="category_detail"),
    
    # Cart endpoints
    path("cart/", CartListCreateApi.as_view(), name="cart-list"),
    path("cart/<int:pk>/", CartRetrieveUpdateDestroyApi.as_view(), name="cart-detail"),
    path("cart/<int:cart_id>/items/", CartItemListCreateApi.as_view(), name="cartitem-list"),
    path("cart/<int:cart_id>/items/<int:pk>/", CartItemRetrieveUpdateDestroyApi.as_view(), name="cartitem-detail"),
    
    # New endpoint for stock status
    path("products/<int:pk>/stock/", ProductStockStatusApi.as_view(), name="product-stock-status"),
]
