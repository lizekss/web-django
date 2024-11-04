from django.contrib.auth.views import LoginView
from django.urls import path

from store.views import RegisterView, CustomLogoutView

app_name = 'user'

urlpatterns = [path('login/', LoginView.as_view(template_name='login.html'), name='login'),
               path('register/', RegisterView.as_view(template_name='register.html'),
                    name='register'),
               path('logout/', CustomLogoutView.as_view(), name='logout'),]
