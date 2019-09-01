import json

import requests
import time
from django.shortcuts import render

host = "5.9.110.169"  # Address of elastic search node
port = "9200"  # Elastic search rest api port
index = "page"


def query_builder(search):
    query_object = {
        "_source": ["title", "url", "lang", "category"],
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "text": {
                                "query": search.query,
                                "boost": 4.0
                            }
                        }
                    },
                    {
                        "match": {
                            "title": {
                                "query": search.query,
                                "boost": 10.0
                            }
                        }
                    },
                    {
                        "match": {
                            "url": {
                                "query": search.query,
                                "boost": 10.0
                            }
                        }
                    },
                    {
                        "match": {
                            "h1List": {
                                "query": search.query,
                                "boost": 8.0
                            }
                        }
                    },
                    {
                        "match": {
                            "h2List": {
                                "query": search.query,
                                "boost": 7.0
                            }
                        }
                    },
                    {
                        "match": {
                            "h3to6List": {
                                "query": search.query,
                                "boost": 6.0
                            }
                        }
                    },
                    {
                        "match": {
                            "metaTags": {
                                "query": search.query,
                                "boost": 5.0
                            }
                        }
                    }
                ]
            }
        },
        "highlight": {
            "number_of_fragments": 1,
            "fragment_size": 250,
            "fields": {
                "text": {"pre_tags": ["<b>"], "post_tags": ["</b>"]}
            }
        }
    }

    if search.language is not None:
        query_object['query']['bool']['filter'] = {
            "term": {
                "lang.keyword": search.language
            }
        }
    return query_object


def search_query(search):
    query = query_builder(search)
    start_time = time.time()
    res = requests.post("http://%s:%s/%s/_search" % (host, port, index), headers={
        "Content-Type": "application/json"
    }, json=query)
    count = res.json()['hits']['total']
    i = 0
    while count > 100:
        count //= 10
        i += 1

    result = {
        "searchTime": time.time() - start_time,
        "resultCount": count * (10 ** i),
        "items": []
    }
    for hit in res.json()['hits']['hits']:
        text = ""
        try:
            text = hit['highlight']['text'][0]
        except:
            pass
        item = {
            "title": hit['_source']['title'],
            "url": hit['_source']['url'],
            "text": text
        }
        if "lang" in hit['_source']:
            item['lang'] = hit['_source']['lang']

        result['items'].append(item)
    return result
    # return {'searchTime': 80.98666048049927, 'resultCount': 55000, 'items': [{'title': 'Informacje Skyscanner o lotnisku Dar es Salam', 'url': 'https://www.skyscanner.pl/lotniska/dar/dar-es-salam-lotnisko.html', 'text': 'Znajdź dane kontaktowe do lotniska Dar es <b>Salam</b> oraz szczegóły na temat linii lotniczych obsługujących loty do i z lotniska Dar es <b>Salam</b>.'}, {'title': 'Aéroport Dar es Salam | Skyscanner', 'url': 'https://www.skyscanner.fr/aeroports/dar/dar-es-salam-aeroport.html', 'text': "Dar es <b>Salam</b> sans avoir besoin de saisir de dates spécifiques ni même de destinations, ce qui fait de lui le meilleur site pour trouver des vols pas chers pour votre voyage vers l'aéroport de Dar es <b>Salam</b>."}, {'title': 'Tanka Tate Salam Songs, Oriya Film Videos | Movie Poster, Wallpapers', 'url': 'http://incredibleorissa.com/oriyafilms/tanka-tate-salam-songs-oriya-film-videos-movie-poster-wallpapers/', 'text': '– Chandan Kar, Rali Nanda Lyricists – Music Director – Abhijit Majumdar Singers – Cinematographer – Story – Nirmal Nayak Screenplay – Dialogues – Editor –To listen and download Tanka Tate <b>Salam</b> Songs, Visit our Oriya Songs Site.Tanka Tate <b>Salam</b> Oriya'}, {'title': 'Rabb al Salam financial definition of Rabb al Salam', 'url': 'https://financial-dictionary.thefreedictionary.com/Rabb+al+Salam', 'text': 'visitors served11,734,320,909Search /Page toolsPage toolsLanguage:Twitter+Sign up with one click:DictionaryThesaurusMedical DictionaryLegal DictionaryFinancial DictionaryAcronymsIdiomsEncyclopediaWikipedia EncyclopediaLanguage:(redirected from Rabb al <b>Salam</b>'}, {'title': 'Maya Salam', 'url': 'https://www.nytimes.com/by/maya-salam', 'text': 'Today, 49 percent believe that, according to Gallup polls.By Maya <b>Salam</b>“The great thing about the last two years is I feel empowered to speak out even further.'}, {'title': '3 Cara untuk Mengeringkan Daun Salam - wikiHow', 'url': 'https://id.wikihow.com/Mengeringkan-Daun-Salam', 'text': 'FacebookMemuat...GoogleMemuat...Akun wikiHowDalam Artikel Ini:Memetik Daun SalamMengeringkan Daun <b>Salam</b> secara AlamiMengeringkan Daun <b>Salam</b> dengan DehidratorReferensiDalam Artikel Ini:Daun <b>salam</b> tumbuh dari pohon dengan nama yang sama, dan bisa ditemukan'}, {'title': '**** AL SALAM HOTEL SUITES, DUBAI ****', 'url': 'https://al-salam-hotel-suites.hotels-in-dubai.org/en/', 'text': 'Hotel Suites DubaiAl <b>Salam</b> Hotel Suites DubaiAl <b>Salam</b> Hotel Suites DubaïAl <b>Salam</b> Hotel Suites DubáiAl <b>Salam</b> Hotel Suites DubaiAl <b>Salam</b> Hotel Suites DubaiAl <b>Salam</b> Hotel Suites DubaiAl <b>Salam</b> Hotel Suites DubaiAl <b>Salam</b> Hotel Suites DubaiAl <b>Salam</b> Hotel Suites'}, {'title': 'Bay al Salam financial definition of Bay al Salam', 'url': 'https://financial-dictionary.thefreedictionary.com/Bay+al+Salam', 'text': ''}, {'title': 'SUBULUS SALAM TERJEMAH PDF', 'url': 'http://playcity.info/subulus-salam-terjemah-49/', 'text': '18 Feb Subulus <b>Salam</b> Terjemahan Pdf 63 ->>> Kitab Tarjamah Subulus <b>Salam</b> Pesantren Library Pustaka. Diantara. 25 Sep Download Subulus <b>Salam</b> Terjemahan apk for Android.'}, {'title': '3r Salam teksty piosenek, tłumaczenia piosenek - Teksciory.pl', 'url': 'https://teksciory.interia.pl/3r-salam,a,28634.html', 'text': '3r Salam3r <b>Salam</b>»Dodaj tekstpodziel sie swoim tłumaczeniemDodaj tekstInteria.pl'}]}

