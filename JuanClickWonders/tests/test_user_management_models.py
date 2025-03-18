import pytest
from django.contrib.auth import get_user_model
from UserManagement.models import UserProfile

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@test.com',
            password='testpassword123'
        )
        assert user.email == 'test@test.com'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password('testpassword123')

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpassword123'
        )
        assert admin.email == 'admin@test.com'
        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_user_str_method(self):
        user = User.objects.create_user(
            email='test@test.com',
            password='testpassword123'
        )
        assert str(user) == 'test@test.com'


@pytest.mark.django_db
class TestUserProfileModel:
    def test_user_profile_creation(self):
        user = User.objects.create_user(
            email='test@test.com',
            password='testpassword123'
        )
        profile = UserProfile.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            phone_number='09995557777',
            address='Quezon City'
        )
        assert profile.first_name == 'Test'
        assert profile.last_name == 'User'
        assert profile.phone_number == '09995557777'
        assert profile.address == 'Quezon City'
        assert profile.user.email == 'test@test.com'

    def test_profile_str_method(self):
        user = User.objects.create_user(
            email='test@test.com',
            password='testpassword123'
        )
        profile = UserProfile.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            phone_number='09995557777',
            address='Quezon City'
        )
        assert str(profile) == 'Test User'