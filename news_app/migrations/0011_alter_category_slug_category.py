# Generated by Django 4.2.6 on 2023-11-06 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news_app", "0010_category_slug_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug_category",
            field=models.SlugField(max_length=30, unique=True),
        ),
    ]
