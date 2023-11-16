from django.urls import path, include

from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('subcategory', SubCategoryViewSet, basename='subcategory')
router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
