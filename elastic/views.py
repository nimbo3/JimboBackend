import json

import requests
import time
from django.shortcuts import render

host = "5.9.110.169"    # Address of elastic search node
port = "9200"           # Elastic search rest api port
index = "page"


def search_query(search):
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
                                "query": search.query
                            }
                        }
                    },
                    {
                        "match": {
                            "title": {
                                "query": search.query
                            }
                        }
                    },
                    {
                        "match": {
                            "url": {
                                "query": search.query
                            }
                        }
                    },
                    {
                        "match": {
                            "h1List": {
                                "query": search.query
                            }
                        }
                    },
                    {
                        "match": {
                            "h2List": {
                                "query": search.query
                            }
                        }
                    },
                    {
                        "match": {
                            "h3to6List": {
                                "query": search.query
                            }
                        }
                    },
                    {
                        "match": {
                            "metaTags": {
                                "query": search.query
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
