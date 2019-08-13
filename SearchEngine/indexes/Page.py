from elasticsearch_dsl import Document
from elasticsearch_dsl import Text


class Page(Document):
    title = Text(analyzer="english")
    text = Text(analyzer="english")
    metaTags = Text(analyzer="english")
    h1List = Text(analyzer="english")
    h2List = Text(analyzer="english")
    h3to6List = Text(analyzer="english")
    url = Text()
