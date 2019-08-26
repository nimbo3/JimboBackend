import json
from _ast import keyword

from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from SearchEngine.models import Search
from elastic.views import search_query


def index(request):
    query = request.GET.get("q")
    language = request.GET.get("lang")
    category = request.GET.get("cat")
    user = None

    token_header = request.headers.get("authorization")
    print(token_header)
    token = Token.objects.filter(key=token_header)
    print(token)
    if len(token) != 0:
        user = token[0].user

    search = Search(query=query, language=language, category=category, user=user)

    search.save()  # Saving search query

    result = search_query(search)
    search.result = result
    search.save()  # Saving search result

    return HttpResponse(json.dumps(result), content_type="application/json")
