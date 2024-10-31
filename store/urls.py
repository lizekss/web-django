from django.contrib.auth.views import LoginView
from django.urls import path
from urllib3 import request

from . import views
from .views import CategoryListView, HomeView, ProductDetailView, ContactView, RegisterView, logout_view

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('category/', CategoryListView.as_view(), name='all_products'),
    path('category/<slug:slug>/', CategoryListView.as_view(),
         name='category_listing'),
    path('product/<int:pk>/',
         ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterView.as_view(template_name='register.html'),
         name='register'),
    path('logout/', logout_view, name='logout'),
]
