from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import RegisterViewSet, LoginViewSet, ChangePasswordViewSet, EmailVerificationViewSet
from accounts.views import HomeView

urlpatterns = [
    path('', HomeView, name='home'),
    path('register', RegisterViewSet.as_view(), name='registeration'),
    path('login', LoginViewSet.as_view(), name='login'),
    path('changepassword', ChangePasswordViewSet.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('resetpassword', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('verify/', EmailVerificationViewSet.as_view(), name='verify_email'),
]
