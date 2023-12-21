from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_tracking.mixins import LoggingMixin

from products.models import Category, SubCategory, Product
from products.serializers import CategorySerializer, CategoryListSerializer
from products.serializers import SubCategorySerializer, SubCategoryListSerializer
from products.serializers import ProductSerializer, ProductListSerializer
from products.utlis import Checking_Product


class CategoryViewSet(ViewSet, LoggingMixin):
    
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)
    
    def get_queryset(self):
        return Category.objects.all()
    
    def list(self, request):
        serializer = CategoryListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = CategoryListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        request_data = {
            'category_name': request.data.get('category_name'),
        }
        
        try:
            category = Category.objects.get(category_name__icontains=request_data['category_name'])
            if category:
                return Response({'status': 'error', 'message': 'Category already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = CategorySerializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            response = {
                'status': 'success',
                'message': "Category created successfully",
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'category_name': request.data.get('category_name', instance.category_name),
        }
        
        serializer = CategorySerializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'status': 'success',
            'message': "Category updated successfully",
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            'status': 'success',
            'message': "Category deleted successfully",
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)   

class SubCategoryViewSet(ViewSet,LoggingMixin):
    def get_object(self, pk):
        return get_object_or_404(SubCategory, pk=pk)
    
    def get_queryset(self):
        return SubCategory.objects.all()
    
    def list(self, request):
        serializer = SubCategoryListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = SubCategoryListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        
        request_data = {
            'subcategory_name': request.data.get('subcategory_name'),
            'category': request.data.get('category')
        }
        
        try:
            subcategory = SubCategory.objects.get(subcategory_name__icontains=request_data['subcategory_name'])
            if subcategory:
                return Response({'status': 'error', 'message': 'SubCategory already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = SubCategorySerializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            response = {
                'status': 'success',
                'message': "SubCategory created successfully",
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'subcategory_name': request.data.get('subcategory_name', instance.subcategory_name),
            'category': request.data.get('category', instance.category)
        }
        
        serializer = SubCategorySerializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'status': 'success',
            'message': "SubCategory updated successfully",
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            'status': 'success',
            'message': "SubCategory deleted successfully",
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
class ProductViewSet(ViewSet, LoggingMixin):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)
    
    def get_queryset(self):
        return Product.objects.all()
    
    def list(self, request):
        vendor = request.query_params.get('vendor')
        products = self.get_queryset()
        if vendor:
            products = products.filter(created_by=vendor)
        else:
            products = products.filter(created_by=request.user.id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = ProductListSerializer(instance)
        instance.view_count += 1
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.user_type == 'customer':
            return Response({"status": "error", "message": "You are not allowed to create product"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        request_data = {
            'name': request.data.get('name'),
            'mfg_date': request.data.get('mfg_date'),
            'price': request.data.get('price'),
            'price_unit': request.data.get('price_unit', "default"),
            'description': request.data.get('description'),
            'subcategory': request.data.get('subcategory'),
            'hashtags': request.data.get('hashtags'),
            'created_by': request.user.id,
        }
        
        images = request.FILES.getlist('images')
        
        context = {
            'images': images,
        }
        
        serializer = ProductSerializer(data=request_data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': 'success',
            'message': "Product created successfully",
        }
        
        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'name': request.data.get('name', instance.name),
            'mfg_date': request.data.get('mfg_date', instance.mfg_date),
            'price': request.data.get('price', instance.price),
            'price_unit': request.data.get('price_unit', instance.price_unit),
            'description': request.data.get('description', instance.description),
            'subcategory': request.data.get('subcategory', instance.subcategory.id),
            'hashtags': request.data.get('hashtags', instance.hashtags),
            'updated_by': request.user.id,
        }
        
        images = request.FILES.getlist('images')
        
        context = {
            'images': images,
        }
        
        serializer = ProductSerializer(instance, data=request_data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'status': 'success',
            'message': "Product updated successfully",
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            'status': 'success',
            'message': "Product deleted successfully",
        }
        
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class ProductListingViewSet(ViewSet, LoggingMixin):
    def list(self, request):
        product = request.query_params.get('product')
        filters = []
        if product:
            filters.append(Q(name__icontains=product) | Q(subcategory__subcategory_name__icontains=product) | Q(subcategory__category__category_name__icontains=product) | Q(hashtags__icontains=product))
        
        products = Product.objects.all()
        
        if product:
            products = products.filter(*filters)
            if not products:
                Checking_Product(product, request.user)
            
        serializer = ProductListSerializer(products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
