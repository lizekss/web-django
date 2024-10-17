from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserCart
from user.models import MyUser


@receiver(post_save, sender=MyUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserCart.objects.create(user=instance)
