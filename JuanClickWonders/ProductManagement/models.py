from django.db import models
from UserManagement.models import UserProfile
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    brand = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    sold_products = models.IntegerField()
    image_url = models.ImageField(upload_to="product_images/", null=False)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Rating(models.Model):
    product = models.ForeignKey("Products", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.ImageField(
        upload_to="rating_images/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="cart"
    )
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        "Cart", on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey("Products", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('GCS', 'GCash'),
    ]

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        "Cart", on_delete=models.CASCADE
    )
    method = models.CharField(max_length=3, choices=PAYMENT_METHODS)
    amount = models.FloatField()
    ref_id = models.CharField(max_length=255)
    success = models.BooleanField(default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="orders"
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ORDER_STATUSES = [
        ('P', 'Paid'),
        ('S', 'To Ship'),
        ('R', 'To Receive'),
        ('D', 'Delivered'),
    ]
    status = models.CharField(
        max_length=1, choices=ORDER_STATUSES, default='P')

    def __str__(self):
        return f"Order {self.order_id}"


class Wishlist(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='wishlist'
    )
    products = models.ManyToManyField(
        Products, related_name='wishlisted_by'
    )

    def __str__(self):
        return f"{self.user}'s Wishlist"
