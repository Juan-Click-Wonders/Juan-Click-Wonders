import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ProductManagement.models import Products, Category, Rating
from UserManagement.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestRatingModels:
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

    def test_rating_creation(self, setup_data):
        rating = Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=5,
            description="Excellent product!"
        )
        assert rating.rating == 5
        assert rating.description == "Excellent product!"
        assert rating.product == self.product
        assert rating.user == self.profile

    def test_rating_invalid_score(self, setup_data):
        with pytest.raises(ValidationError):
            rating = Rating.objects.create(
                product=self.product,
                user=self.profile,
                rating=6,
                description="Invalid rating"
            )
            rating.full_clean()

        with pytest.raises(ValidationError):
            rating = Rating.objects.create(
                product=self.product,
                user=self.profile,
                rating=0,
                description="Invalid rating"
            )
            rating.full_clean()

    def test_multiple_ratings_same_product(self, setup_data):
        Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=4,
            description="Good product"
        )

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

        Rating.objects.create(
            product=self.product,
            user=other_profile,
            rating=5,
            description="Excellent product"
        )

        assert Rating.objects.filter(product=self.product).count() == 2

    def test_rating_cascade_delete(self, setup_data):
        rating = Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=4,
            description="Good product"
        )

        # Test if rating is deleted when product is deleted
        self.product.delete()
        assert Rating.objects.filter(id=rating.id).exists() is False

        # Create new rating and test if it's deleted when user is deleted
        new_product = Products.objects.create(
            name='New Product',
            description='New Description',
            brand='Test Brand',
            price=100.00,
            stock=10,
            sold_products=0,
            category=self.category
        )
        new_rating = Rating.objects.create(
            product=new_product,
            user=self.profile,
            rating=4,
            description="Good product"
        )
        self.profile.delete()
        assert Rating.objects.filter(id=new_rating.id).exists() is False