import pytest
from django.utils import timezone
from ProductManagement.models import Payment, Cart
from UserManagement.models import UserProfile, User


@pytest.fixture
def create_user(db):
    return User.objects.create_user(
        email='test.user@test.com',
        password='SecurePassword123'
    )


@pytest.fixture
def create_user_profile(create_user):
    return UserProfile.objects.create(
        user=create_user,
        first_name='Young',
        last_name='Sleepy Boi',
        phone_number='09123456789',
        address='Quezon City, Philippines'
    )


@pytest.fixture
def create_cart(create_user_profile):
    return Cart.objects.create(user=create_user_profile)


@pytest.mark.django_db
class TestPaymentModel:
    def test_create_payment_cod(self, create_user_profile, create_cart):
        payment = Payment.objects.create(
            user=create_user_profile,
            cart=create_cart,
            method='COD',
            amount=1000.00,
            success=True,
        )

        assert payment.method == 'COD'
        assert payment.amount == 1000.00
        assert payment.success is True
        assert payment.user == create_user_profile
        assert payment.cart == create_cart
        assert payment.timestamp <= timezone.now()

    @pytest.mark.parametrize("method", ['GCS', 'MYA'])
    def test_create_payment_other_method(self, create_user_profile, create_cart, method):
        payment = Payment.objects.create(
            user=create_user_profile,
            cart=create_cart,
            method=method,
            amount=500.00,
            success=False,
        )

        assert payment.method == method
        assert payment.amount == 500.00
