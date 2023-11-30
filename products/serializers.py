from rest_framework import serializers

from products.models import Category, SubCategory, Product, ProductImages

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CategoryListSerializer(serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField()
    
    def get_subcategory(self, obj):
        data = SubCategory.objects.filter(category=obj)
        return SubCategorySerializer(data, many=True).data
    
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'subcategory']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name', 'category']

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name',	'mfg_date',	'price', 'price_unit', 'description', 'hashtags', 'created_by', 'subcategory', 'updated_by']
        extra_kwargs = {
            'created_by' : {"write_only": True},
            'updated_by' : {"write_only": True},
        }
    
    def save(self, **kwargs):
        product = super().save()
        image_files = self.context.get("images")
        if image_files:
            files = [
                ProductImages(image=file, product=product) for file in image_files
            ]
            ProductImages.objects.bulk_create(files)
        return product
    
class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'image']

class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        data = ProductImages.objects.filter(product=obj)
        return ProductImagesSerializer(data, many=True).data
    
    class Meta:
        model = Product
        fields = ['id', 'name',	'mfg_date',	'price', 'price_unit', 'description', 'hashtags', 'created_by', 'subcategory', 'images']
        