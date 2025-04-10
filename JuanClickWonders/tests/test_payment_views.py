import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from UserManagement.models import User, UserProfile
from ProductManagement.models import Cart, CartItem, Products, Category, Payment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_with_profile(db):
    user = User.objects.create_user(
        email='wowtest@wow.com',
        password='YesVerySecure321'
    )
    profile = UserProfile.objects.create(
        user=user,
        first_name='Juan',
        last_name='Dela Cruz',
        phone_number='09998887777',
        address='Makati City, Philippines'
    )
    return user


@pytest.fixture
def authenticated_client(api_client, user_with_profile):
    api_client.force_authenticate(user=user_with_profile)
    return api_client


@pytest.fixture
def cart(user_with_profile):
    return Cart.objects.create(user=user_with_profile.profile)


@pytest.fixture
def product():
    category = Category.objects.create(category_name='Electronics')
    return Products.objects.create(
        name='Laptop',
        description='Many RGB lights wow',
        brand='ASUS',
        price=40000.00,
        stock=10,
        sold_products=0,
        image_url='product_images/laptop.jpg',
        category=category
    )


@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=2
    )


@pytest.mark.django_db
class TestPaymentView:
    def test_cod_payment_success(self, authenticated_client, cart, cart_item):
        response = authenticated_client.post(
            "http://127.0.0.1:8000/payment/",
            {"method": "COD"},
            format='json'
        )

        assert response.status_code == 200
        assert response.data['message'] == "Payment is now being processed via COD."
        assert Payment.objects.count() == 1
        assert CartItem.objects.filter(cart=cart).count() == 0

    def test_payment_with_invalid_method(self, authenticated_client, cart):
        response = authenticated_client.post(
            "http://127.0.0.1:8000/payment/",
            {"method": "WOW"},
            format='json'
        )

        assert response.status_code == 400
        assert response.data["error"] == "Invalid or missing payment method."
        assert Payment.objects.count() == 0

    def test_payment_with_empty_cart(self, authenticated_client, cart):
        response = authenticated_client.post(
            "http://127.0.0.1:8000/payment/",
            {"method": "COD"},
            format='json'
        )

        assert response.status_code == 400
        assert response.data["error"] == "The cart is empty."

    @pytest.mark.parametrize("method, channel_code", [
        ("GCS", "GCASH"),
        ("MYA", "PAYMAYA")
    ])
    def test_ewallet_payment_success(self, authenticated_client, cart, cart_item, mocker, method, channel_code):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "actions": [{
                "url_type": "WEB",
                "url": f"https://xendit.link/{channel_code.lower()}"
            }]
        }
        mocker.patch("ProductManagement.views.PaymentAPI.process_ewallet_payment",
                     return_value=mock_response)

        response = authenticated_client.post(
            "http://127.0.0.1:8000/payment/",
            {"method": method},
            format='json'
        )

        assert response.status_code == 200
        assert "action_url" in response.data
        assert Payment.objects.count() == 1

    @pytest.mark.parametrize("method", ["GCS", "MYA"])
    def test_ewallet_payment_failure(self, authenticated_client, cart, cart_item, mocker, method):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"error": "Payment failed."}
        mocker.patch("ProductManagement.views.PaymentAPI.process_ewallet_payment",
                     return_value=mock_response)

        response = authenticated_client.post(
            "http://127.0.0.1:8000/payment/",
            {"method": method},
            format='json'
        )

        assert response.status_code == 400
        assert response.data["message"] == "Payment failed."
        assert Payment.objects.count() == 1

    def test_unauthenticated_payment(self, api_client):
        response = api_client.post(
            "http://127.0.0.1:8000/payment/",
            {"method": "COD"},
            format='json'
        )
        assert response.status_code == 401
