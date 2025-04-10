import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ProductManagement.models import Products, Category, Rating
from UserManagement.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile
import django.core.exceptions

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

        self.product.delete()
        assert Rating.objects.filter(id=rating.id).exists() is False

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

    def test_rating_with_image(self, setup_data):
        image = SimpleUploadedFile(
            name="review.jpg",
            content=b"fakeimagecontent",
            content_type="image/jpeg"
        )
        rating = Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=4,
            description="Good product with image",
            image_url=image
        )
        
        assert rating.image_url.name.startswith('rating_images/')
        assert 'review' in rating.image_url.name
        assert rating.image_url.name.endswith('.jpg')
        assert Rating.objects.filter(image_url__isnull=False).count() == 1

    def test_rating_without_image(self, setup_data):
        # Image is now optional, so this should work without raising an error
        rating = Rating.objects.create(
            product=self.product,
            user=self.profile,
            rating=4,
            description="Good product without image",
            image_url=None
        )
        assert not rating.image_url
        assert str(rating.image_url) == ''
        assert Rating.objects.filter(image_url='').count() == 1

    def test_rating_with_invalid_image_url(self, setup_data):
        with pytest.raises(ValidationError):
            rating = Rating.objects.create(
                product=self.product,
                user=self.profile,
                rating=4,
                description="Good product",
                image_url="invalid-url"
            )
            rating.full_clean()
