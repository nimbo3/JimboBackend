import json

from django.http import HttpResponse

from elastic.views import search


def index(request):
    query = request.GET["q"]
    result = search(query)
    return HttpResponse(json.dumps(result), content_type="application/json")
