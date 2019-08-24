import json

from django.http import HttpResponse

from SearchEngine.models import Search
from elastic.views import search_query


def index(request):
    query = request.GET.get("q")
    language = request.GET.get("lang")
    category = request.GET.get("cat")
    search = Search(query=query, language=language, category=category)
    if request.user.is_authenticated:
        search.user = request.user
    search.save()  # Saving search query

    result = search_query(search)
    search.result = result
    search.save()  # Saving search result

    return HttpResponse(json.dumps(result), content_type="application/json")
