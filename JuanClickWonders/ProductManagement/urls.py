from django.urls import path
from ProductManagement import views
from ProductManagement.views import (
    CartItemListCreateApi, 
    CartItemRetrieveUpdateDestroyApi, 
    CartListCreateApi, 
    CartRetrieveUpdateDestroyApi,
    ProductStockStatusApi,
    ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView, CategoryListView, CategoryCreateView, CategoryDetailView, CategoryDetailUpdateDeleteView
)

urlpatterns = [
    path('products/', views.ProductListCreateApi.as_view()),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path("products/<int:pk>/stock/", ProductStockStatusApi.as_view(), name="product-stock-status"),
    # path('ratings/', RatingsListView.as_view(), name='ratings-list'),
    # path('ratings/create/', RatingsCreateView.as_view(), name='ratings-create'),
    # path('ratings/<int:pk>/', RatingsDetailUpdateDeleteView.as_view(), name='ratings-detail-update-delete'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/update/<int:pk>/', CategoryDetailUpdateDeleteView.as_view(), name='category-detail-update-delete'),
    
    # Cart endpoints
    path("cart/", CartListCreateApi.as_view(), name="cart-list"),
    path("cart/<int:pk>/", CartRetrieveUpdateDestroyApi.as_view(), name="cart-detail"),
    path("cart/<int:cart_id>/items/", CartItemListCreateApi.as_view(), name="cartitem-list"),
    path("cart/<int:cart_id>/items/<int:pk>/", CartItemRetrieveUpdateDestroyApi.as_view(), name="cartitem-detail"),
    
    
]
