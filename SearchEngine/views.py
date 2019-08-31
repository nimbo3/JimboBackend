import json
from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token

from SearchEngine.models import Search
from elastic.views import search_query


def index(request):
    query = request.GET.get("q")
    language = request.GET.get("language")
    category = request.GET.get("category")
    user = None

    token_header = request.headers.get("authorization")
    token = Token.objects.filter(key=token_header)
    if len(token) != 0:
        user = token[0].user

    search = Search(query=query, language=language, category=category, user=user, search_time=datetime.now())

    search.save()  # Saving search query

    result = search_query(search)
    search.result = result
    search.save()  # Saving search result

    return HttpResponse(json.dumps(result), content_type="application/json")


def history(request):
    user = None

    token_header = request.headers.get("authorization")
    token = Token.objects.filter(key=token_header)
    if len(token) != 0:
        user = token[0].user
    if user is None:
        return HttpResponse(json.dumps({
            "Error": "you not logged in"
        }), status=401)

    today_first_second = datetime(year=datetime.now().year,
                                  month=datetime.now().month,
                                  day=datetime.now().day,
                                  hour=0, minute=0, second=0)

    last_7_day_first_second = today_first_second - timedelta(days=6)
    last_30_day_first_second = today_first_second - timedelta(days=29)
    search_history_today = Search.objects.filter(
        user=user,
        search_time__range=[today_first_second, datetime.now()]
    ).values('query', 'search_time', 'language', 'category', 'id')
    search_history_this_week = Search.objects.filter(
        user=user,
        search_time__range=[last_7_day_first_second, today_first_second]
    ).values('query', 'search_time', 'language', 'category', 'id')
    search_history_this_month = Search.objects.filter(
        user=user,
        search_time__range=[last_30_day_first_second, last_7_day_first_second]
    ).values('query', 'search_time', 'language', 'category', 'id')

    return JsonResponse({
        "today": list(reversed(list(search_history_today))),
        "week": list(reversed(list(search_history_this_week))),
        "month": list(reversed(list(search_history_this_month)))
    }, safe=False)
