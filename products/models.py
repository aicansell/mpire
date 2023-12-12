import json
from django.db import models

from Common.models import Common

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        ordering = ['category_name']


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subcategory_name
    
    class Meta:
        ordering = ['subcategory_name']

class Product(Common):
    PRICE_UNIT_CHOICES = (
        ("piece", "Piece"),
        ("unit", "Unit"),
        ("default", "Default")
    )

    name = models.CharField(max_length=100)
    mfg_date = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    price_unit = models.CharField(max_length=40, choices=PRICE_UNIT_CHOICES, default="default")
    description = models.TextField()
    hashtags = models.CharField(max_length=200, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.CASCADE)
    view_count = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product"

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to="media/products/images")

    def __str__(self):
        return self.product.name
