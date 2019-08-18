from django.db import models


class Search(models.Model):

    LANGUAGE_CHOICES = (
        (0, ''),
    )

    CATEGORY_CHOICES = (
        (0, 'Sport'),
        (1, 'Sport'),
        (2, 'Sport'),
        (3, 'Sport'),
        (4, 'Sport'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    query = models.CharField(max_length=512, null=False)
    language = models.IntegerField(null=True)
    category = models.IntegerField(null=True)
