# Generated by Django 2.2.4 on 2019-08-31 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SearchEngine', '0004_auto_20190827_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='category',
            field=models.CharField(choices=[('economics', 'Economics'), ('health', 'Health'), ('sport', 'Sport'), ('technology', 'Technology'), ('art', 'Art')], max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='language',
            field=models.CharField(choices=[('ar', 'Arabic'), ('de', 'German'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('fa', 'Farsi'), ('ru', 'Russian')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='search_time',
            field=models.DateTimeField(null=True),
        ),
    ]