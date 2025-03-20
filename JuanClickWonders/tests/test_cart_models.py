import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from ProductManagement.models import Products, Category, Cart, CartItem
from UserManagement.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestCartModels:
    @pytest.fixture
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

    def test_cart_creation(self, setup_data):
        cart = Cart.objects.create(user=self.profile)
        assert cart.user == self.profile
        assert cart.cart_items.count() == 0

    def test_cart_item_creation(self, setup_data):
        cart = Cart.objects.create(user=self.profile)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        assert cart_item.quantity == 2
        assert cart_item.product == self.product
        assert cart_item.cart == cart

    def test_multiple_cart_items(self, setup_data):
        cart = Cart.objects.create(user=self.profile)
        additional_product = Products.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            brand='Test Brand',
            price=200.00,
            stock=5,
            sold_products=0,
            category=self.category
        )
        
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        CartItem.objects.create(cart=cart, product=additional_product, quantity=1)
        
        assert cart.cart_items.count() == 2
        assert sum(item.quantity for item in cart.cart_items.all()) == 3

    def test_cart_item_constraints(self, setup_data):
        cart = Cart.objects.create(user=self.profile)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=1
        )
        
        with pytest.raises(IntegrityError):
            CartItem.objects.create(
                cart=cart,
                product=self.product,
                quantity=-1 
            )
