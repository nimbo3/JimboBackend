from django.db import models
import json


class Page:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.text = kwargs.get("text")
        self.h1List = kwargs.get("h1List")
        self.h2List = kwargs.get("h2List")
        self.h3To6List = kwargs.get("h3To6List")
        self.metaTags = kwargs.get("metaTags")

    def __str__(self):
        return json.dump(self)