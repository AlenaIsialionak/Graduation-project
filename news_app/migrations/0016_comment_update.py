# Generated by Django 4.2.6 on 2023-11-06 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0015_alter_article_options_alter_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
