# Generated by Django 4.2.6 on 2023-11-07 19:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news_app", "0019_likecomment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="likes",
            field=models.ManyToManyField(
                related_name="likes_comment", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="LikeComment",
        ),
    ]
