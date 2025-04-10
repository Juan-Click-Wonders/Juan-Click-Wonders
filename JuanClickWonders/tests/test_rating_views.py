import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ProductManagement.models import Products, Category, Rating
from UserManagement.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestRatingViews:
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

    def test_create_rating(self, setup_data):
        url = reverse('ratings-create')
        data = {
            'user': self.user.id,
            'product': self.product.product_id,
            'rating': 4,
            'description': 'Great product!'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Rating.objects.count() == 1
        assert Rating.objects.first().rating == 4

    def test_create_invalid_rating(self, setup_data):
        url = reverse('ratings-create')
        data = {
            'product': self.product.product_id,
            'rating': 6,  # Invalid rating > 5
            'description': 'Invalid rating'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_ratings(self, setup_data):
        # Create some ratings
        Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=4,
            description="Good product"
        )
        
        url = reverse('ratings-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_filter_ratings_by_product(self, setup_data):
        Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=4,
            description="Good product"
        )
        
        url = reverse('ratings-list')
        response = self.client.get(f"{url}?product={self.product.product_id}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_update_rating(self, setup_data):
        rating = Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=3,
            description="Initial review"
        )
        
        url = reverse('ratings-detail-update-delete', kwargs={'pk': rating.pk})
        data = {
            'rating': 4,
            'description': 'Updated review'
        }
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        rating.refresh_from_db()
        assert rating.rating == 4
        assert rating.description == 'Updated review'

    def test_delete_rating(self, setup_data):
        rating = Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=3,
            description="Test review"
        )
        
        url = reverse('ratings-detail-update-delete', kwargs={'pk': rating.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Rating.objects.count() == 0

    def test_unauthorized_access(self, setup_data):
        # Test without authentication
        self.client.force_authenticate(user=None)
        url = reverse('ratings-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_other_user_rating(self, setup_data):
        # Create another user and their rating
        other_user = User.objects.create_user(
            email='other@test.com',
            password='testpass123'
        )
        other_profile = UserProfile.objects.create(
            user=other_user,
            first_name='Other',
            last_name='User',
            phone_number='09995557778',
            address='Other Address'
        )
        rating = Rating.objects.create(
            product=self.product,
            user=other_profile,
            rating=3,
            description="Other user's review"
        )
        
        url = reverse('ratings-detail-update-delete', kwargs={'pk': rating.pk})
        data = {
            'rating': 4,
            'description': 'Trying to update'
        }
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN