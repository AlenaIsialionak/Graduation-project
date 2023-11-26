# Generated by Django 4.2.6 on 2023-11-12 15:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_app', '0021_article_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ManyToManyField(related_name='favorite_art', to=settings.AUTH_USER_MODEL),
        ),
    ]