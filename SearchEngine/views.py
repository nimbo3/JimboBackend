from django.http import HttpResponse
import json


def search(request):
    query = request.GET.get("q")

    if query is None or query is "":
        return HttpResponse(json.dumps({
            "search": ""
        }))

    return HttpResponse(query)


def index(request):
    return HttpResponse("salam")
