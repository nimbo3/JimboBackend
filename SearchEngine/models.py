from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


class Search(models.Model):

    LANGUAGE_CHOICES = (
        (0, 'ar'),
        (1, 'de'),
        (2, 'en'),
        (3, 'es'),
        (4, 'fr'),
        (5, 'fa'),
        (6, 'ru'),
    )

    CATEGORY_CHOICES = (
        (0, 'sport'),
        (1, 'health'),
        (2, 'news'),
        (3, 'cat4'),
        (4, 'cat5'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    query = models.CharField(max_length=512, null=False)
    language = models.IntegerField(null=True, choices=LANGUAGE_CHOICES)
    category = models.IntegerField(null=True, choices=CATEGORY_CHOICES)
    result = JSONField()

