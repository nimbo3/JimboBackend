import json

from django.http import HttpResponse

from SearchEngine.models import Search
from elastic.views import search_query


def index(request):
    query = request.GET.get("q")
    language = request.GET.get("lang")
    category = request.GET.get("cat")
    search = Search(query=query, language=language, category=category)
    search.save()
    result = search_query(search)
    return HttpResponse(json.dumps(result), content_type="application/json")
