import json, requests
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


def complete(request):
    # response = requests.get("http://localhost:1478/suggest?suggest=" + request.GET.get("q"))
    response = requests.get("http://46.4.40.237:1478/suggest?suggest=" + request.GET.get("q"))
    print("autocomplete request: " + response.text)
    return JsonResponse(response.json(), safe=False)


def top_pages(request):
    category = request.GET.get("category")
    url = "http://server-master:1478/top?category=" + category
    response = requests.get(url)
    return JsonResponse(response.json(), safe=False)


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


def suggestion(request):
    user = None
    token_header = request.headers.get("authorization")
    token = Token.objects.filter(key=token_header)
    if len(token) != 0:
        user = token[0].user
    if user is None:
        return HttpResponse(json.dumps({
            "Error": "you not logged in"
        }), status=401)

    technology_count = len(Search.objects.filter(user=user, category="technology"))
    art_count = len(Search.objects.filter(user=user, category="art"))
    sport_count = len(Search.objects.filter(user=user, category="sports"))
    health_count = len(Search.objects.filter(user=user, category="health"))
    economics_count = len(Search.objects.filter(user=user, category="economics"))

    category_list = tuple(reversed(sorted((
        (technology_count, "technology"),
        (art_count, "art"),
        (sport_count, "sports"),
        (health_count, "health"),
        (economics_count, "economics")
    ))))

    return JsonResponse({
        "suggest": category_list[0][1]
    })
