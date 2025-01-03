from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    product_link = models.URLField(max_length=200, blank=True, null=True)
    rate = models.CharField(max_length=10, blank=True, null=True)
    consideration_num = models.CharField(max_length=10, blank=True, null=True)
    seller = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sizes = models.JSONField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)

    def image_link(self):
        first_image = self.images.first()
        return first_image.image_url if first_image else "No Image"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return self.image_url
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name="favorited")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price