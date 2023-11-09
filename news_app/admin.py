from django.contrib import admin

from .models import Category, Article, Content

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Content)
# Register your models here.
