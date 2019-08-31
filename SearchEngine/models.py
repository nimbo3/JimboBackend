from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


class Search(models.Model):

    LANGUAGE_CHOICES = (
        ('ar', 'Arabic'),
        ('de', 'German'),
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('fa', 'Farsi'),
        ('ru', 'Russian'),
    )

    CATEGORY_CHOICES = (
        ('economics', 'Economics'),
        ('health', 'Health'),
        ('sport', 'Sport'),
        ('technology', 'Technology'),
        ('art', 'Art'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    query = models.CharField(max_length=512, null=False)
    language = models.CharField(null=True, max_length=3, choices=LANGUAGE_CHOICES)
    category = models.CharField(null=True, max_length=11, choices=CATEGORY_CHOICES)
    search_time = models.DateTimeField(null=True)
    result = JSONField()
