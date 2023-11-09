from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse



class Category(models.Model):
    topic = models.CharField(max_length=50)
    number = models.IntegerField()
    update = models.DateTimeField(auto_now=True)
    slug_category = models.SlugField(max_length=30, unique=True, db_index=True)
    def __str__(self):
        return self.topic + '|' + f'{self.number}'

    class Meta:
        default_related_name = 'categories'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug_category': self.slug_category})



class Article(models.Model):
    title = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    slug_article = models.SlugField(max_length=30, unique=True, db_index=True)

    class Meta:
        default_related_name = 'articles' # for object


class Content(models.Model):
    story = models.TextField()
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='content')


class LikeArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_art')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes_art')


class DislikeArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes_art')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='dislikes_art')


class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    data = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes_comment')


# class LikeComment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_comment')
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes_comment')
#
#
# class DislikeComment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_comment')
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes_comment')
