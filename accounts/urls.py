from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    url('account-create', views.UserCreate.as_view(), name='account-create'),
    url('account-login', views.UserLogin.as_view(), name='account-login'),
    # url(r'^api/v1/', include('rest_framework.urls', namespace='rest_framework'))
]

