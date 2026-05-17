# ads/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Must be exactly 'urlpatterns' (all lowercase, no underscores)
urlpatterns = [
    path('', views.home, name='home'),
    path('owner/login/', auth_views.LoginView.as_view(
        template_name='ads/login.html',
        success_url='/owner/dashboard/'  # Add this line
    ), name='login'),
    path('owner/logout/', views.owner_logout, name='logout'),
    path('owner/dashboard/', views.owner_dashboard, name='dashboard'),
    path('owner/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('owner/edit/<int:pk>/', views.edit_product, name='edit_product'),
]