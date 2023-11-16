from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from products.models import Category, SubCategory, Product
from products.serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, ProductListSerializer


class CategoryViewSet(ViewSet,LoggingMixin):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)
    
    def get_queryset(self):
        return Category.objects.all()
    
    def list(self, request):
        serializer = CategorySerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubCategoryViewSet(ViewSet,LoggingMixin):
    def get_object(self, pk):
        return get_object_or_404(SubCategory, pk=pk)
    
    def get_queryset(self):
        return SubCategory.objects.all()
    
    def list(self, request):
        serializer = SubCategorySerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductViewSet(ViewSet,LoggingMixin):

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)
    
    def get_queryset(self):
        return Product.objects.all()
    
    def list(self, request):
        serializer = ProductListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = ProductListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

