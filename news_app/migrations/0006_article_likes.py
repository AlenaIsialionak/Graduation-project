# Generated by Django 4.2.6 on 2023-11-02 11:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news_app", "0005_rename_content_content_story"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="likes",
            field=models.ManyToManyField(
                related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
