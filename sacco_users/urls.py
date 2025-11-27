from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('api/users/', views.UserListCreateView.as_view(), name='api_user-list-create'),
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='api_user-detail'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('add-user/', views.add_user_view, name='add_user'),
    path('edit-user/<int:pk>/', views.edit_user_view, name='edit_user'),
    path('delete-user/<int:pk>/', views.delete_user_view, name='delete_user'),
    path('scan/', views.scan_view, name='scan'),
]
