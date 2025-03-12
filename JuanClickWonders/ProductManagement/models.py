from django.db import models


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


# class Rating(models.Model):
#     product = models.ForeignKey("Products", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField()
#     description = models.TextField()
#     created_at = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.product.name}: {self.rating}"
