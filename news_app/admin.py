from django.contrib import admin

from .models import Category, Article, Content, Language

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Content)
admin.site.register(Language)
# Register your models here.
