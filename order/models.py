from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import MyUser
from store.models import Product

from django.utils.translation import gettext_lazy as _


class UserCart(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return _("Cart of %s") % self.user

    class Meta:
        verbose_name = _('UserCart')
        verbose_name_plural = _('UserCarts')


class CartItem(models.Model):
    cart = models.ForeignKey(
        UserCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return _("%f of %s in %s's cart") % (self.quantity, self.product, self.cart.user)

    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = _('CartItem')
        verbose_name_plural = _('CartItems')


@receiver(post_save, sender=MyUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserCart.objects.create(user=instance)
