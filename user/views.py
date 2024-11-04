from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from user.models import MyUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('email', 'date_of_birth')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
