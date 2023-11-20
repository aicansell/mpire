from django.urls import path, include

from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet, VendorViewSet

router = DefaultRouter()
router.register("user", UserViewSet, basename="user")
router.register("vendor", VendorViewSet, basename="vendor")


urlpatterns = [
    path("", include(router.urls))
]
