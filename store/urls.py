from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf.urls import handler500

from . import views
from .views import CategoryListView, HomeView, ProductDetailView, ContactView, RegisterView, \
    CustomLogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('category/', CategoryListView.as_view(), name='all_products'),
    path('category/<slug:slug>/', CategoryListView.as_view(),
         name='category_listing'),
    path('product/<int:pk>/',
         ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]
