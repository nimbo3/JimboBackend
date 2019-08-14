from django.conf.urls import url
from . import views

urlpatterns = [
    url('api/users', views.UserCreate.as_view(), name='account-create'),
    url('api/users', views.UserLogin.as_view(), name='account-login'),
]
