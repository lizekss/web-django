from django.urls import path
from .views import CartView, CheckoutView, AddToCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
]
