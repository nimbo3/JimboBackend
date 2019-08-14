from django.conf.urls import url
from . import views

urlpatterns = [
    url('users', views.UserCreate.as_view(), name='account-create'),
    url('users', views.UserLogin.as_view(), name='account-login'),
]
