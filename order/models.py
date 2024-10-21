from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import MyUser


class UserCart(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name='cart')


@receiver(post_save, sender=MyUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserCart.objects.create(user=instance)
