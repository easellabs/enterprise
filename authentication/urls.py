# Updated urls.py

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import register_user, login_user, enable_2fa, verify_2fa

# Authentication URLs
auth_patterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('enable-2fa/', enable_2fa, name='enable_2fa'),
    path('verify-2fa/', verify_2fa, name='verify_2fa'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Main URLs with versioning
urlpatterns = [
    path('api/v1/auth/', include((auth_patterns, 'authentication'), namespace='auth')),
]
