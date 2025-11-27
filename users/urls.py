from django.urls import path
from . import views
from sacco_users.views import profile_view

urlpatterns = [
    path('<int:pk>/', profile_view, name='user_detail'),
]
