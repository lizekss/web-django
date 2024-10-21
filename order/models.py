from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import MyUser
from store.models import Product


class UserCart(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        UserCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user}'s cart"

    def get_total_price(self):
        return self.product.price * self.quantity


@receiver(post_save, sender=MyUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserCart.objects.create(user=instance)
