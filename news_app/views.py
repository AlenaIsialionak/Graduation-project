from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from news_app.models import Article, Content, Category, Comment, LikeArticle
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from news_app.forms import CommentForm
from django.db.models import Count
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def main_page(request: HttpRequest):
    count = User.objects.count()
    return render(request, 'main.html', {
        'count': count
    })


class MainView(ListView):
    model = Category
    template_name = 'main.html'


def get_article(request, slug_category):
    category = get_object_or_404(Category, slug_category=slug_category)
    all_articles = category.articles.all()
    list_article = [a for a in all_articles]
    return render(request, 'description_of_category.html', context={'articles': list_article, 'category': category})




def sign_up(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request,
                  'registration/signup.html',
                  {'form': form})



def like_article(request: HttpResponse, slug_category, slug_article):
    article = get_object_or_404(Article, slug_article=slug_article)
    user_ = request.user
    users_like = LikeArticle.objects.filter(user=user_, article=article)
    if request.method == 'POST':
        if not users_like:
            LikeArticle.objects.create(article=article, user=user_)
        else:
            users_like.delete()

    return redirect('article', slug_category, slug_article)


def like_comment(request: HttpResponse, slug_category, slug_article, pk: int):
    comment = get_object_or_404(Comment, pk=pk)
    user_ = request.user
    us = User.objects.get(username=user_)
    having_like = comment.likes.filter(username=user_)

    if request.method == 'POST':
        if not having_like:
            comment.likes.add(us)

        else:
            comment.likes.remove(us)

    return redirect('article', slug_category, slug_article)





def dislike(request):
    pass


def search_for_article(request):
    pass

def _get_story(art):
    story = art.content
    form = CommentForm()

    return story


def _add_comment(comment_data: dict):
    comment_form = CommentForm(data=comment_data)

    if comment_form.is_valid():
        comment_dict = Comment.objects.create(
            content=comment_data.get('content'),
            article=comment_data.get('article'),
            user=comment_data.get('user'),
            data=comment_data.get('data')
        )
    comment_form = CommentForm()
    return comment_form

def _update_comment(comment_data: dict, pk: int, comment_form):

    if comment_form.is_valid():
        comment_dict = Comment.objects.filter(pk=pk).update(
            content=comment_data.get('content'),
            data=comment_data.get('data')
        )
    comment_form = CommentForm()
    return comment_form



def update_comment(request: HttpResponse, slug_category, slug_article, pk: int ):
    comment = get_object_or_404(Comment, id=pk)
    form = CommentForm(instance=comment)
    art = get_object_or_404(Article, slug_article=slug_article)


    if request.method == 'POST':

        comment_data = {
            'content': request.POST.get('content')
        }
        comment_form = CommentForm(data=comment_data)
        if comment_form.is_valid():
            comment_dict = Comment.objects.filter(pk=pk).update(
            content=comment_data.get('content')
            )

            return redirect('article', slug_category, slug_article)

    return render(
        request,
        'update_comment.html',
        context={'article': art,
                 'form': form,
                 'slug_category': slug_category,
                 'slug_article': slug_article,
                 'comment': comment})


def delete_comment(request: HttpResponse, pk: int, slug_category, slug_article):
    comment = get_object_or_404(Comment, id=pk)
    art_pk = comment.article.pk
    comment.delete()
    return redirect('article', slug_category, slug_article)

# def get_story_and_comments(request: HttpResponse, slug_category, slug_article):




def get_story_and_comments(request: HttpResponse, slug_category, slug_article):
    art = get_object_or_404(Article, slug_article=slug_article)
    story = _get_story(art)
    comments = art.comments.all().order_by('data')
    comment_form = CommentForm()
    likes_article = (LikeArticle.objects.values('article_id').
             filter(article_id=art).
             annotate(number=Count('article_id')))

    if like := [a for a in likes_article]:
        likes_article = like[0].get('number')
    else:
        likes_article = 0
    amount_of_comments = []
    for comment in comments:
        amount = comment.likes.count()
        amount_of_comments.append(amount)

    #
    return render(
        request,
        'story.html',
        context={'story_': story,
                 'article': art,
                 'comments': comments,
                 'slug_category': slug_category,
                 'form': comment_form,
                 'likes_article': likes_article,
                 'a': request.user.pk,
                 'amount_of_comments': amount_of_comments})

def delete_comment(request: HttpResponse, pk: int, slug_category, slug_article):
    comment = get_object_or_404(Comment, id=pk)
    art_pk = comment.article.pk
    comment.delete()
    return redirect('article', slug_category, slug_article)


def add_comment(request: HttpResponse, slug_category, slug_article):
    art = get_object_or_404(Article, slug_article=slug_article)
    comments = art.comments.all()

    # Add comment
    if request.method == 'POST':
        comment_data = {
            'content': request.POST.get('content'),
            'data': request.POST.get('data'),
            'article': art,
            'user': request.user
        }
        comment_form = _add_comment(comment_data)
    else:
        comment_form = CommentForm()

    return render(
        request,
        'story.html',
        context={'article': art,
                 'form': comment_form,
                 'comments': comments,
                 'slug_category': slug_category})





# def sign_in(request: HttpRequest):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(
#                 request,
#                 'user_forms.html',
#                 context={'form': form}
#             )


# def get_story_and_add_comment(request: HttpResponse, slug_category, slug_article):
#     art = get_object_or_404(Article, slug_article=slug_article)
#     comments = art.comments.all()
#
#     # Add comment
#     if request.method == 'POST':
#         comment_data = {
#             'content': request.POST.get('content'),
#             'data': request.POST.get('data'),
#             'article': art,
#             'user': request.user
#         }
#         comment_form = _add_comment(comment_data)
#     else:
#         comment_form = CommentForm()
#
#     # Get story
#     story = _get_story(art)
#     return render(
#         request,
#         'story.html',
#         context={'story_': story,
#                  'article': art,
#                  'form': comment_form,
#                  'comments': comments,
#                  'slug_category': slug_category})




# def get_update_comment(request: HttpResponse, comment_id: int):
# class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Comment
#     template_name = 'story.html'
#     form_class = CommentForm
#
#     def form_valid(self, form):
#         comment = get_object_or_404(Comment, id=self.kwargs['pk'])
#         form.instance.user = self.request.user
#         form.instanse.comment = comment
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_success_url(self):
#         slug_category = self.kwargs['slug_category']
#         slug_article = self.kwargs['slug_article']
#         return redirect('main')
#
#     def test_func(self):
#         comment = self.get_object()
#         if self.request.user == comment.user:
#             return True
#         return False


# class DescriptionOfCategory(DetailView):
#     model = Category
#     template_name = 'description_of_category.html'
