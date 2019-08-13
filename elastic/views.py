import requests
from django.shortcuts import render

host = "144.76.119.111"
port = "9200"
index = "page"


def search(query):
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
    return res.text
