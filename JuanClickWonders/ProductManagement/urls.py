from django.urls import path
from ProductManagement.views import (
    ProductListCreateApi,
    ProductDetailApi,
    CategoryListCreateApi,
    CategoryDetailApi,
    CartItemListCreateApi,
    CartItemRetrieveUpdateDestroyApi,
    CartListCreateApi,
    CartRetrieveUpdateDestroyApi,
    ProductStockStatusApi,
    RatingsCreateView,
    RatingsListView,
    RatingsDetailUpdateDeleteView,
    PaymentAPI,
)

urlpatterns = [
    path("products/", ProductListCreateApi.as_view(), name="product_list"),
    path("products/<int:product_id>",
         ProductDetailApi.as_view(), name="product_detail"),
    path('products/create/', ProductListCreateApi.as_view(), name='product_create'),
    path('products/update/<int:product_id>/',
         ProductDetailApi.as_view(), name='product_update'),
    path('products/delete/<int:product_id>/',
         ProductDetailApi.as_view(), name='product_delete'),
    path("products/<int:product_id>/stock/",
         ProductStockStatusApi.as_view(), name="product_stock_status"),
    path("category/", CategoryListCreateApi.as_view(), name="category_list"),
    path('category/create/', CategoryListCreateApi.as_view(), name='category_create'),
    path("category/<int:category_id>", CategoryDetailApi.as_view(), name="category_detail"),
    path('category/update/<int:category_id>/', CategoryDetailApi.as_view(), name='category-detail-update-delete'),
    
  
    path('ratings/', RatingsListView.as_view(), name='ratings-list'),
    path('ratings/create/', RatingsCreateView.as_view(), name='ratings-create'),
    path('ratings/<int:pk>/', RatingsDetailUpdateDeleteView.as_view(), name='ratings-detail-update-delete'),
    
    path("category/<int:category_id>",
         CategoryDetailApi.as_view(), name="category_detail"),
    path('category/update/<int:category_id>/',
         CategoryDetailApi.as_view(), name='category-detail-update-delete'),

    path("cart/", CartListCreateApi.as_view(), name="cart-list"),
    path("cart/<int:pk>/", CartRetrieveUpdateDestroyApi.as_view(), name="cart-detail"),
    path("cart/<int:cart_id>/items/",
         CartItemListCreateApi.as_view(), name="cartitem-list"),
    path("cart/<int:cart_id>/items/<int:pk>/",
         CartItemRetrieveUpdateDestroyApi.as_view(), name="cartitem-detail"),
    path("payment/", PaymentAPI.as_view(), name="payment")
]
