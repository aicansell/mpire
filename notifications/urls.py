from django.urls import path, include

from rest_framework.routers import DefaultRouter

from notifications.views import NotificationViewSet, MessageViewSet

router1 = DefaultRouter()
router2 = DefaultRouter()

router1.register('', NotificationViewSet, basename='notification')
router2.register('', MessageViewSet, basename='messages')

urlpatterns = [
    path('noti/', include(router1.urls)),
    path('msg/', include(router2.urls)),
]
