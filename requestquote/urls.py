from django.urls import path, include

from rest_framework.routers import DefaultRouter

from requestquote.views import RequestQuoteViewSet

router = DefaultRouter()

router.register('', RequestQuoteViewSet, basename='requestquote')

urlpatterns = [
    path('', include(router.urls)),
]
