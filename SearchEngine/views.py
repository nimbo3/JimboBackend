from django.http import HttpResponse
import json

from elastic.views import search


def index(request):
    return HttpResponse(search(request.GET.get("q")), content_type="application/json")


def login(request):
    return None


def register(request):
    return None