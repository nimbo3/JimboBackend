import json

import requests
import time
from django.shortcuts import render

host = "5.9.110.169"  # Address of elastic search node
port = "9200"  # Elastic search rest api port
index = "page"


def query_builder(search):
    query_object = {
        "_source": ["title", "url", "lang"],
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
    print(query_object)
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
        result['items'].append({
            "title": hit['_source']['title'],
            "url": hit['_source']['url'],
            "text": text
        })
    return result
