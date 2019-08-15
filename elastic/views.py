import json

import requests
import time
from django.shortcuts import render

host = "144.76.119.111"
port = "9200"
index = "page"


def search(query):
    start_time = time.time()
    res = requests.post("http://%s:%s/%s/_search" % (host, port, index), headers={
        "Content-Type": "application/json"
    }, json={
        "_source": ["title", "url"],
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "text": {
                                "query": query
                            }
                        }
                    },
                    {
                        "match": {
                            "title": {
                                "query": query
                            }
                        }
                    },
                    {
                        "match": {
                            "url": {
                                "query": query
                            }
                        }
                    },
                    {
                        "match": {
                            "h1List": {
                                "query": query
                            }
                        }
                    },
                    {
                        "match": {
                            "h2List": {
                                "query": query
                            }
                        }
                    },
                    {
                        "match": {
                            "h3to6List": {
                                "query": query
                            }
                        }
                    },
                    {
                        "match": {
                            "metaTags": {
                                "query": query
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
    })
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
