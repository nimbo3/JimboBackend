from django.http import HttpResponse
import json


def search(request):
    query = request.GET.get("q")

    if query is None or query is "":
        return json.dumps({
            "search"
        })

    return HttpResponse(query)