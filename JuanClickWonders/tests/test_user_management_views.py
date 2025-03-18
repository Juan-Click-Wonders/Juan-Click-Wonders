import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from UserManagement.models import UserProfile

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'email': 'test@test.com',
        'password1': 'mypassword123!',
        'password2': 'mypassword123!',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '09995557777',
        'address': 'Quezon City'
    }


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        email='test@test.com', password='mypassword123!')
    UserProfile.objects.create(
        user=user,
        first_name='Test',
        last_name='User',
        phone_number='09995557777',
        address='Quezon City'
    )
    return user


@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.mark.django_db
class TestRegisterView:
    def test_register_success(self, api_client, user_data):
        url = reverse('register')
        response = api_client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=user_data['email']).exists()
        user = User.objects.get(email=user_data['email'])
        assert UserProfile.objects.filter(user=user).exists()

    def test_register_passwords_dont_match(self, api_client, user_data):
        user_data['password2'] = 'ImTiredBoss456!'
        url = reverse('register')
        response = api_client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
        assert not User.objects.filter(email=user_data['email']).exists()

    def test_register_email_already_exists(self, api_client, user_data, test_user):
        url = reverse('register')
        response = api_client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data


@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self, api_client, test_user):
        url = reverse('login')
        data = {
            'email': 'test@test.com',
            'password': 'mypassword123!'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert settings.SIMPLE_JWT['AUTH_COOKIE'] in response.cookies
        assert settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'] in response.cookies
        assert response.data['message'] == 'Login successful.'

    def test_login_invalid_credentials(self, api_client):
        url = reverse('login')
        data = {
            'email': 'pagod.me@test.com',
            'password': 'notreal789!'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert settings.SIMPLE_JWT['AUTH_COOKIE'] not in response.cookies
        assert settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'] not in response.cookies


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_success(self, authenticated_client, mocker):
        mocker.patch('UserManagement.views.RefreshToken')
        url = reverse('logout')
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']].value == ''
        assert response.cookies[settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']].value == ''
        assert response.data['message'] == 'Logout successful.'

    def test_logout_inauthenticated(self, api_client):
        url = reverse('logout')
        response = api_client.post(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserView:
    def test_get_authenticated_user(self, authenticated_client, test_user):
        url = reverse('user-retrieve')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == test_user.email

    def test_get_inauthenticated_user(self, api_client):
        url = reverse('user-retrieve')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfileView:
    def test_get_authenticated_profile(self, authenticated_client, test_user):
        url = reverse('profile-retrieve')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == test_user.email
        assert response.data['first_name'] == 'Test'
        assert response.data['last_name'] == 'User'
        assert response.data['phone_number'] == '09995557777'
        assert response.data['address'] == 'Quezon City'

    def test_get_inauthenticated_profile(self, api_client):
        url = reverse('profile-retrieve')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateProfileView:
    def test_update_profile_success(self, authenticated_client, test_user):
        url = reverse('profile-update')
        data = {
            'email': 'updated@test.com',
            'phone_number': '09995554444',
            'address': 'Makati City',
            'current_password': 'mypassword123!'
        }
        response = authenticated_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        test_user.refresh_from_db()
        assert test_user.email == 'updated@test.com'
        profile = UserProfile.objects.get(user=test_user)
        assert profile.phone_number == '09995554444'
        assert profile.address == 'Makati City'

    def test_update_profile_wrong_password(self, authenticated_client):
        url = reverse('profile-update')
        data = {
            'email': 'updated@test.com',
            'phone_number': '09995554444',
            'address': 'Makati City',
            'current_password': 'BroImSleepy789!'
        }
        response = authenticated_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'current_password' in response.data

    def test_update_profile_email_already_exists(self, authenticated_client, db):
        user = User.objects.create_user(
            email='existingtest@test.com', password='wowpassword123!'
        )
        UserProfile.objects.create(
            user=user,
            first_name='Existing',
            last_name='User',
            phone_number='09995551111',
            address='Pasig City'
        )

        url = reverse('profile-update')
        data = {
            'email': 'existingtest@test.com',
            'phone_number': '09995554444',
            'address': 'Makati City',
            'current_password': 'mypassword123!'
        }
        response = authenticated_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data


@pytest.mark.django_db
class TestUpdatePasswordView:
    def test_update_password_success(self, authenticated_client, test_user):
        url = reverse('user-update-password')
        data = {
            'current_password': 'mypassword123!',
            'new_password': 'newpassword456!',
            'confirm_new_password': 'newpassword456!'
        }
        response = authenticated_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Password updated successfully.'

        test_user.refresh_from_db()
        assert test_user.check_password('newpassword456!')

    def test_update_password_wrong_current_password(self, authenticated_client):
        url = reverse('user-update-password')
        data = {
            'current_password': 'WantToHave8hrsSleep!',
            'new_password': 'newpassword456!',
            'confirm_new_password': 'newpassword456!'
        }
        response = authenticated_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'current_password' in response.data

    def test_update_password_password_dont_match(self, authenticated_client):
        url = reverse('user-update-password')
        data = {
            'current_password': 'mypassword123!',
            'new_password': 'newpassword456!',
            'confirm_new_password': 'IForgorMyPassAgain!'
        }
        response = authenticated_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'new_password' in response.data


@pytest.mark.django_db
class TestDeleteUserView:
    def test_delete_user_success(self, authenticated_client, test_user, mocker):
        mocker.patch('UserManagement.views.RefreshToken')
        url = reverse('user-delete')
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=test_user.id).exists()

    def test_delete_user_inauthenticated(self, api_client):
        url = reverse('user-delete')
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestForgotPasswordView:
    def test_forgot_password_success(self, api_client, test_user, mocker):
        mock_send_mail = mocker.patch('UserManagement.views.send_mail')
        url = reverse('forgot-password')
        data = {
            'email': 'test@test.com'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Password reset email sent. Please check your inbox.'
        mock_send_mail.assert_called_once()

    def test_forgot_password_email_not_found(self, api_client):
        url = reverse('forgot-password')
        data = {
            'email': 'antok.test@test.com'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data


@pytest.mark.django_db
class TestResetPasswordView:
    def test_reset_password_success(self, api_client, test_user):
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = reverse('reset-password')
        data = {
            'uidb64': uidb64,
            'token': token,
            'new_password': 'BagongPassword789!',
            'confirm_new_password': 'BagongPassword789!'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Password reset successfully.'
        test_user.refresh_from_db()
        assert test_user.check_password('BagongPassword789!')

    def test_reset_password_invalid_user_id(self, api_client, test_user):
        uidb64 = 'invaliduidb64'
        token = default_token_generator.make_token(test_user)
        url = reverse('reset-password')
        data = {
            'uidb64': uidb64,
            'token': token,
            'new_password': 'BagongPassword789!',
            'confirm_new_password': 'BagongPassword789!'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'user' in response.data

    def test_reset_password_invalid_token(self, api_client, test_user):
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = 'invalidtoken'
        url = reverse('reset-password')
        data = {
            'uidb64': uidb64,
            'token': token,
            'new_password': 'BagongPassword789!',
            'confirm_new_password': 'BagongPassword789!'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' in response.data

    def test_reset_password_passwords_dont_match(self, api_client, test_user):
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = reverse('reset-password')
        data = {
            'uidb64': uidb64,
            'token': token,
            'new_password': 'BagongPassword789!',
            'confirm_new_password': 'MyMemoryBad456!'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'new_password' in response.data


@pytest.mark.django_db
class TestTokenRefreshView:
    def test_token_refresh_success(self, api_client, test_user, mocker):
        mock_refresh = mocker.MagicMock()
        mock_refresh.access_token = 'new_access_token'
        mock_refresh.__getitem__.side_effect = lambda key: test_user.id if key == 'user_id' else None
        mock_refresh_class = mocker.patch(
            'UserManagement.views.RefreshToken', return_value=mock_refresh
        )
        mocker.patch(
            'UserManagement.views.User.objects.get',
            return_value=test_user
        )

        new_refresh = mocker.MagicMock()
        new_refresh.__str__.return_value = 'new_refresh_token'
        mocker.patch('UserManagement.views.RefreshToken.for_user',
                     return_value=new_refresh)
        api_client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
                           ] = 'old_refresh_token'

        url = reverse('refresh-token')
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Token refreshed successfully.'
        assert settings.SIMPLE_JWT['AUTH_COOKIE'] in response.cookies
        assert settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'] in response.cookies
        mock_refresh_class.assert_called_once_with('old_refresh_token')

    def test_token_refresh_no_token(self, api_client):
        url = reverse('refresh-token')
        response = api_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'No refresh token found.'

    def test_token_refresh_invalid_token(self, api_client, mocker):
        mocker.patch('UserManagement.views.RefreshToken',
                     side_effect=TokenError('Invalid or expired token.')
                     )
        api_client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
                           ] = 'invalid_token'

        url = reverse('refresh-token')
        response = api_client.post(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['error'] == 'Invalid or expired token.'