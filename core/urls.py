from django.urls import path
from .views import register_account, home

urlpatterns = [
    path('register/', register_account, name='register'),
    path('', home, name='home')
]