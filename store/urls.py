from django.urls import path
from . import views
from .views import CategoryListView

# urlpatterns = [
#     path('products/', views.product_list, name='product_list'),
#     path('category/<int:category_id>/products',
#          views.category_detail, name='category_detail'),
# ]

urlpatterns = [
    path('', views.index, name="index"),
    path('category/', CategoryListView.as_view(), name='all_products'),
    path('category/<slug:slug>/', CategoryListView.as_view(),
         name='category_listing'),
    path('product/<slug:slug>/',
         views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
]
