import json

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse

from elastic.views import search


def index(request):
    return HttpResponse(search(request.GET.get("q")), content_type="application/json")


def login_view(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    user = User.objects.filter(username=username)


def register_view(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    first_name = request.GET.get("first_name")
    last_name = request.GET.get("last_name")
    if username in None or password is None or first_name is None or last_name is None:
        pass
    user = User(username=username, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    return HttpResponse(json.dumps({

    }))
