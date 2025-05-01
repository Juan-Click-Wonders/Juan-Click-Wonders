import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from UserManagement.models import User, UserProfile
from ProductManagement.models import Products, Category, Order


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_with_profile(db):
    user = User.objects.create_user(
        email='testuser@example.com',
        password='SecurePassword123'
    )
    profile = UserProfile.objects.create(
        user=user,
        first_name='Test',
        last_name='User',
        phone_number='09998887777',
        address='Test Address'
    )
    return user


@pytest.fixture
def staff_user(db):
    user = User.objects.create_user(
        email='staffuser@example.com',
        password='StaffPassword123',
        is_staff=True
    )
    profile = UserProfile.objects.create(
        user=user,
        first_name='Staff',
        last_name='User',
        phone_number='09998887777',
        address='Staff Address'
    )
    return user


@pytest.fixture
def authenticated_client(api_client, user_with_profile):
    api_client.force_authenticate(user=user_with_profile)
    return api_client


@pytest.fixture
def staff_authenticated_client(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    return api_client


@pytest.fixture
def product():
    category = Category.objects.create(category_name='Electronics')
    return Products.objects.create(
        name='Smartphone',
        description='Latest model',
        brand='Samsung',
        price=30000.00,
        stock=20,
        sold_products=5,
        image_url='product_images/smartphone.jpg',
        category=category
    )


@pytest.fixture
def order(user_with_profile, product):
    return Order.objects.create(
        user=user_with_profile.profile,
        product=product,
        quantity=2,
        status='P'  # Paid status
    )


@pytest.mark.django_db
class TestOrderStatusUpdate:
    def test_update_order_status(self, authenticated_client, order):
        url = f'/orders/{order.order_id}/status/'
        response = authenticated_client.put(
            url,
            {"status": "S"},  # Change to "To Ship" status
            format='json'
        )

        assert response.status_code == 200
        assert response.data['message'] == "Order status updated to To Ship."
        
        # Verify the order status was updated in the database
        updated_order = Order.objects.get(order_id=order.order_id)
        assert updated_order.status == "S"

    def test_update_order_status_to_delivered(self, authenticated_client, order):
        url = f'/orders/{order.order_id}/status/'
        response = authenticated_client.put(
            url,
            {"status": "D"},  # Change to "Delivered" status
            format='json'
        )

        assert response.status_code == 200
        assert response.data['message'] == "Order status updated to Delivered."
        
        # Verify the order status was updated in the database
        updated_order = Order.objects.get(order_id=order.order_id)
        assert updated_order.status == "D"

    def test_update_order_status_invalid_status(self, authenticated_client, order):
        url = f'/orders/{order.order_id}/status/'
        response = authenticated_client.put(
            url,
            {"status": "X"},  # Invalid status
            format='json'
        )

        assert response.status_code == 400
        assert "Invalid status" in response.data['error']

    def test_update_order_status_missing_status(self, authenticated_client, order):
        url = f'/orders/{order.order_id}/status/'
        response = authenticated_client.put(
            url,
            {},  # Missing status
            format='json'
        )

        assert response.status_code == 400
        assert response.data['error'] == "New status is required."

    def test_update_nonexistent_order(self, authenticated_client):
        url = '/orders/9999/status/'  # Non-existent order ID
        response = authenticated_client.put(
            url,
            {"status": "S"},
            format='json'
        )

        assert response.status_code == 404
        assert response.data['error'] == "Order not found."

    def test_update_order_status_unauthenticated(self, api_client, order):
        url = f'/orders/{order.order_id}/status/'
        response = api_client.put(
            url,
            {"status": "S"},
            format='json'
        )

        assert response.status_code == 401  # Unauthorized
