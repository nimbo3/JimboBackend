from django.conf.urls import url
from . import views

urlpatterns = [
    url('account-create', views.UserCreate.as_view(), name='account-create'),
    url('account-login', views.UserLogin.as_view(), name='account-login'),
]

