# Generated by Django 4.2.6 on 2023-11-04 18:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("news_app", "0008_alter_comment_article_alter_comment_data_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={"default_related_name": "article"},
        ),
    ]
