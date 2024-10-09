from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import register_user, login_user, enable_2fa, verify_2fa
from .views import (
    RegisterUserView, RegisterAdminUserView, AdminOnlyView,
    UserProfileView, ListUsersView, ManageUserView,
    UserDashboardView, AdminDashboardView, LogoutView, LoginUserView
)

app_name = 'authentication'  # Add this line for namespacing





# Authentication URLs
auth_patterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register-admin/', RegisterAdminUserView.as_view(), name='register_admin'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# User Management URLs
user_management_patterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', ListUsersView.as_view(), name='list_users'),
    path('users/<int:pk>/', ManageUserView.as_view(), name='manage_user'),
]

# Dashboard URLs
dashboard_patterns = [
    path('user-dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]

# Admin Specific URLs
admin_patterns = [
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
]

# Combine all URL patterns with versioning and logical grouping
urlpatterns = [
    path('api/v1/auth/', include((auth_patterns, app_name), namespace='authentication')),
    path('api/v1/users/', include((user_management_patterns, app_name), namespace='user_management')),
    path('api/v1/dashboards/', include((dashboard_patterns, app_name), namespace='dashboards')),
    path('api/v1/admin/', include((admin_patterns, app_name), namespace='admin')),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('enable-2fa/', enable_2fa, name='enable_2fa'),
    path('verify-2fa/', verify_2fa, name='verify_2fa'),
]
