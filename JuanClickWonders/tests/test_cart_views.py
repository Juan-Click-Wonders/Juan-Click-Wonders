import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from ProductManagement.models import Products, Category, Cart, CartItem
from UserManagement.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestCartViews:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user = User.objects.create_user(
            email='testuser@test.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            phone_number='09995557777',
            address='Test Address'
        )
        
        self.category = Category.objects.create(category_name='Test Category')
        self.product = Products.objects.create(
            name='Test Product',
            description='Test Description',
            brand='Test Brand',
            price=100.00,
            stock=10,
            sold_products=0,
            category=self.category
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_add_duplicate_product(self, setup_data):
        cart = Cart.objects.create(user=self.profile)
        
        response1 = self.client.post(f'/cart/{cart.cart_id}/items/', {
            'product': self.product.product_id,
            'quantity': 2
        })
        assert response1.status_code == 201
    
        response2 = self.client.post(f'/cart/{cart.cart_id}/items/', {
            'product': self.product.product_id,
            'quantity': 3
        })
        assert response2.status_code == 200
        
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        assert cart_item.quantity == 5  # 2 + 3

    def test_unauthorized_access(self, setup_data):
        unauthorized_user = User.objects.create_user(
            email='unauthorized@test.com',
            password='testpass123'
        )
        profile = UserProfile.objects.create(
            user=unauthorized_user,
            first_name='Unauthorized',
            last_name='User',
            phone_number='09995557777',
            address='Fake City'
        )
        unauthorized_client = APIClient()
        unauthorized_client.force_authenticate(user=unauthorized_user)
        cart = Cart.objects.create(user=self.profile)
        
        response = unauthorized_client.get(f'/cart/{cart.cart_id}/')
        assert response.status_code == 404

    def test_invalid_quantity_update(self, setup_data):
        cart = Cart.objects.create(user=self.profile)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=1
        )

        response1 = self.client.patch(
            f'/cart/{cart.cart_id}/items/{cart_item.id}/',
            {'quantity': 0}
        )
        assert response1.status_code == 400

        response2 = self.client.patch(
            f'/cart/{cart.cart_id}/items/{cart_item.id}/',
            {'quantity': -1}
        )
        assert response2.status_code == 400

    def test_invalid_product_id(self, setup_data):
        cart = Cart.objects.create(user=self.profile)
        
        response = self.client.post(f'/cart/{cart.cart_id}/items/', {
            'product': -1, 
            'quantity': 1
        })
        assert response.status_code == 400

    def test_unauthenticated_access(self, setup_data):
        client = APIClient()
        cart = Cart.objects.create(user=self.profile)
        
        response = client.get(f'/cart/{cart.cart_id}/')
        assert response.status_code == 401