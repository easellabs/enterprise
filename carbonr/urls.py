"""
URL configuration for the CarbonR project.

The `urlpatterns` list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/

This configuration includes:
1. Core Admin interface.
2. Authentication APIs.
3. Application-specific APIs.
4. Health check endpoint for monitoring.
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from . import views  # Assuming there is a `views.py` with a health check view

# Customizing the admin URL for security purposes
ADMIN_URL = 'secure-admin/'  # Change this to a unique, non-trivial URL for added security.

urlpatterns = [
    # Admin URL with customization for better security
    path(ADMIN_URL, admin.site.urls),

    # Authentication module URL routing, with namespace for easier identification
    path('auth/', include(('authentication.urls', 'authentication'), namespace='authentication')),

    # API module URL routing, with namespace for easier identification
    path('api/', include(('api.urls', 'api'), namespace='api')),

    # Health Check endpoint for load balancer and application monitoring
    path('health/', views.health_check, name='health_check'),

    # Catch-All Route for handling non-existent URLs - serves a 404 page
    re_path(r'^.*$', TemplateView.as_view(template_name='404.html'), name='404_page'),
]

# Adding detailed comments to guide developers on adding new URLs
"""
URL Patterns:
- `secure-admin/`: Custom path for the Django admin site to enhance security.
- `auth/`: Routes all requests starting with `auth/` to the authentication module.
- `api/`: Routes all requests starting with `api/` to the main application APIs.
- `health/`: A health check endpoint used for monitoring purposes.
- `404_page`: A catch-all route to display a custom 404 page for non-existent URLs.
"""

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from authentication.views import RegisterView, OTPVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('authentication.urls')),
    # Other URLs
]


