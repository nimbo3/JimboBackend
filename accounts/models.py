from django.db import models


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
        (0, 'Sport'),
        (1, 'Health'),
        (2, 'News'),
        (3, 'Cat4'),
        (4, 'Cat5'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    query = models.CharField(max_length=512, null=False)
    language = models.IntegerField(null=True, choices=LANGUAGE_CHOICES)
    category = models.IntegerField(null=True, choices=CATEGORY_CHOICES)
