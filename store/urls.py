from django.urls import path
from . import views
from .views import CategoryListView, HomeView, ProductDetailView, ContactView

# urlpatterns = [
#     path('products/', views.product_list, name='product_list'),
#     path('category/<int:category_id>/products',
#          views.category_detail, name='category_detail'),
# ]

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('category/', CategoryListView.as_view(), name='all_products'),
    path('category/<slug:slug>/', CategoryListView.as_view(),
         name='category_listing'),
    path('product/<int:pk>/',
         ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]
