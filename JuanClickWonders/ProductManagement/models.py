from django.db import models


class Products(models.Model):
    product_ID = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=500)
    price = models.FloatField()
    inventory_level = models.IntegerField()
    description = models.CharField(max_length=1000)
    brand = models.CharField(max_length=500)
    product_image = models.ImageField(upload_to="product_images/", null=False)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )


class Category(models.Model):
    category_ID = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=500)
    category_description = models.CharField(max_length=1000)
