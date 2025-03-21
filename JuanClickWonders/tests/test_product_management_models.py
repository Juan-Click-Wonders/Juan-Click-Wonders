import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from ProductManagement.models import Products, Category

@pytest.fixture
def category():
    return Category.objects.create(category_name="GPU")

@pytest.fixture
def product(category):
    image = SimpleUploadedFile(name="3090.jpg", content=b"fakeimagecontent", content_type="image/jpeg")
    return Products.objects.create(
        name="RTX 3090",
        description="A Powerful GPU for all your needs",
        brand="ASUS",
        price=90000.00,
        stock=14,
        sold_products=10,
        image_url=image,
        category=category
    )

@pytest.mark.django_db
def test_product_creation(product, category):
    assert product.name == "RTX 3090"
    assert product.description == "A Powerful GPU for all your needs"
    assert product.brand == "ASUS"
    assert product.price == 90000.00
    assert product.stock == 14
    assert product.sold_products == 10
    assert product.category == category

@pytest.mark.django_db
def test_category_str(category):
    assert str(category) == "GPU"

@pytest.mark.django_db
def test_product_str(product):
    assert str(product) == "RTX 3090"
