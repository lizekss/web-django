from django.db import models
from user.models import MyUser  # Import your custom user model


class UserCart(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name='cart')
