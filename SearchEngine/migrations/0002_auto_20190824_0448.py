# Generated by Django 2.2.4 on 2019-08-24 04:48

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('SearchEngine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='result',
            field=jsonfield.fields.JSONField(),
        ),
    ]
