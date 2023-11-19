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
        ("Piece", "Piece"),
        ("Unit", "Unit"),
        ("default", "default")
    )

    name = models.CharField(max_length=100)
    mfg_date = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    price_unit = models.CharField(max_length=40, choices=PRICE_UNIT_CHOICES, default="default")
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_description_as_dict(self):
        return json.loads(self.description)
    
    class Meta:
        verbose_name = "Product"

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to="media/products/images")

    def __str__(self):
        return self.product.name
