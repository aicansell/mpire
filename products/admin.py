from django.contrib import admin

from products.models import Category, SubCategory, Product, ProductImages

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImages)