import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from ProductManagement.models import Products, Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def category():
    return Category.objects.create(category_name="GPU")

@pytest.fixture
def product(category):
    image = SimpleUploadedFile("3090.png", b"fakeimagecontent", content_type="image/png")
    return Products.objects.create(
        name="RTX 3090",
        description="High-performance graphics card",
        brand="NVIDIA",
        price=999.99,
        stock=20,
        sold_products=5,
        image_url=image,
        category=category
    )

@pytest.mark.django_db
def test_list_products(api_client, product):
    url = reverse("product_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_search_products(api_client, product):
    url = reverse("product_list") + "?search=RTX"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["name"] == "RTX 3090"

@pytest.mark.django_db
def test_filter_products_by_category(api_client, product):
    url = reverse("product_list") + "?category=GPU"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["category_name"] == product.category.category_name

@pytest.mark.django_db
def test_create_product(api_client, category):
    image_io = BytesIO()
    image = Image.new("RGB", (100, 100), color="white")
    image.save(image_io, format="PNG")
    image_io.seek(0)

    test_image = SimpleUploadedFile("test.png", image_io.getvalue(), content_type="image/png")

    url = reverse("product_create")
    data = {
        "name": "RTX 4080",
        "description": "Next-gen GPU",
        "brand": "NVIDIA",
        "price": 119900.99,
        "stock": 10,
        "sold_products": 2,
        "image_url": test_image, 
        "category": category.category_id,
    }
    response = api_client.post(url, data, format="multipart")
    print("Response Data:", response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "RTX 4080"

@pytest.mark.django_db
def test_get_product_detail(api_client, product):
    url = reverse("product_detail", kwargs={"product_id": product.product_id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == product.name

@pytest.mark.django_db
def test_update_product(api_client, product):
    url = reverse("product_update", kwargs={"product_id": product.product_id})
    data = {"price": 899.99}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["price"] == 899.99

@pytest.mark.django_db
def test_delete_product(api_client, product):
    url = reverse("product_delete", kwargs={"product_id": product.product_id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Products.objects.filter(product_id=product.product_id).count() == 0

@pytest.mark.django_db
def test_list_categories(api_client, category):
    url = reverse("category_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_create_category(api_client):
    url = reverse("category_create")
    data = {"category_name": "Laptops"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["category_name"] == "Laptops"

@pytest.mark.django_db
def test_get_category_detail(api_client, category):
    url = reverse("category_detail", kwargs={"category_id": category.category_id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["category_name"] == category.category_name

@pytest.mark.django_db
def test_update_category(api_client, category):
    url = reverse("category-detail-update-delete", kwargs={"category_id": category.category_id})
    data = {"category_name": "GPUs"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["category_name"] == "GPUs"

@pytest.mark.django_db
def test_delete_category(api_client, category):
    url = reverse("category-detail-update-delete", kwargs={"category_id": category.category_id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.filter(category_id=category.category_id).count() == 0
