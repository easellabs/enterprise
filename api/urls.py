# api/urls.py
from django.urls import path
# from authentication.views import (
#     ListUsersView, ManageUserView, UserDashboardView,
#     AdminDashboardView, AdminOnlyView
# )

app_name = 'api'  # Use app_name for namespacing

urlpatterns = [
    # # Endpoints related to user management
    # path('users/', ListUsersView.as_view(), name='list_users'),
    # path('users/<int:pk>/', ManageUserView.as_view(), name='manage_user'),
    
    # # Dashboard views
    # path('user-dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    # path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # # Admin specific
    # path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
]
