# Generated by Django 4.2.6 on 2023-11-03 19:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news_app", "0006_article_likes"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Review",
            new_name="Comment",
        ),
    ]
