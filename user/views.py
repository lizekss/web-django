from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from user.models import MyUser


# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('email', 'date_of_birth')
