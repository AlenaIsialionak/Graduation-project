from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from news_app.models import (Article, Content, Category,
                             Comment, LikeArticle, Dictionary,
                             Language, Translation, DislikeArticle)
import random
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from news_app.forms import CommentForm, LevelForm, DictionaryForm, LanguageForm, TranslationForm
from django.db.models import Count
from googletrans import Translator
import logging
import sys
from news_app.utils import query_debugger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
           "[%(name)s:%(funcName)s:%(lineno)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
django_logger = logging.getLogger('django.db.backends')
django_logger.setLevel(logging.DEBUG)
django_logger.addHandler(logging.StreamHandler())

def main_page(request: HttpRequest):
    count = User.objects.count()
    return render(request, 'main.html', {
        'count': count
    })

class MainView(ListView):
    model = Category
    template_name = 'main.html'


@query_debugger(logger)
def get_article(request, slug_category):
    category = get_object_or_404(Category, slug_category=slug_category)
    all_articles = category.articles.all()
    # all_articles = category.articles.select_related('category').all()
    logger.warning(f"SQL: {str(all_articles.query)}")
    form_level = LevelForm(request.POST or None)
    lev = 'Nothing'
    level_dict = {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}
    if request.method == 'POST' and form_level.is_valid():
        lev = form_level.cleaned_data.get('levels')
        if lev != 4:
            all_articles = all_articles.filter(level=level_dict.get(lev))
    list_article = [a for a in all_articles]

    return render(
        request,
        'description_of_category.html',
        context={'articles': list_article,
                 'category': category,
                 'form_level': form_level,
                 'level': lev})


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
    user_dislike = DislikeArticle.objects.filter(user=user_, article=article)
    user_like = LikeArticle.objects.filter(user=user_, article=article)
    if request.method == 'POST':
        if user_dislike:
            user_dislike.delete()
            user_like = LikeArticle.objects.create(user=user_, article=article)

            return redirect('article', slug_category, slug_article)

        user_like = LikeArticle.objects.filter(user=user_, article=article)
        if not user_like:
            user_like = LikeArticle.objects.create(user=user_, article=article)
        else:
            user_like.delete()

    return redirect('article', slug_category, slug_article)


def dislike_article(request: HttpResponse, slug_category, slug_article):
    article = get_object_or_404(Article, slug_article=slug_article)
    user = request.user
    user_like = LikeArticle.objects.filter(user=user, article=article)
    if request.method == 'POST':
        if user_like:
            user_like.delete()
            user_dislike = DislikeArticle.objects.create(user=user, article=article)

            return redirect('article', slug_category, slug_article)

        user_dislike = DislikeArticle.objects.filter(user=user, article=article)
        if not user_dislike:
            user_dislike = DislikeArticle.objects.create(user=user, article=article)
        else:
            user_dislike.delete()

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


def _get_story(art):
    story = art.content
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


def get_story_and_comments(request: HttpResponse, slug_category, slug_article):
    art = get_object_or_404(Article, slug_article=slug_article)
    story = _get_story(art)
    comments = art.comments.all().order_by('data')
    comment_form = CommentForm()
    likes_article = (LikeArticle.objects.values('article_id').
                     filter(article_id=art).
                     annotate(number=Count('article_id')))

    dislikes_article = (DislikeArticle.objects.values('article_id').
                        filter(article_id=art).
                        annotate(number=Count('article_id')))

    if like := [a for a in likes_article]:
        likes_article = like[0].get('number')
    else:
        likes_article = 0
    amount_of_comments = []
    if dislike := [a for a in dislikes_article]:
        dislikes_article = dislike[0].get('number')
    else:
        dislikes_article = 0

    amount_of_comments = []
    for comment in comments:
        amount = comment.likes.count()
        amount_of_comments.append(amount)

    return render(
        request,
        'story.html',
        context={'story_': story,
                 'article': art,
                 'comments': comments,
                 'slug_category': slug_category,
                 'form': comment_form,
                 'likes_article': likes_article,
                 'dislikes_article': dislikes_article,
                 'a': request.user.pk,
                 'amount_of_comments': amount_of_comments})


def add_comment(request: HttpResponse, slug_category, slug_article):
    art = get_object_or_404(Article, slug_article=slug_article)
    comments = art.comments.all()

    if request.method == 'POST':
        comment_data = {
            'content': request.POST.get('content'),
            'data': request.POST.get('data'),
            'article': art,
            'user': request.user
        }
        comment_form = _add_comment(comment_data)
        return redirect('article', slug_category, slug_article)
    else:
        comment_form = CommentForm()

    return render(
        request,
        'story.html',
        context={'article': art,
                 'form': comment_form,
                 'comments': comments,
                 'slug_category': slug_category
                 }
    )


def add_favorite_article(request, slug_article, slug_category):
    art = get_object_or_404(Article, slug_article=slug_article)
    user_ = request.user
    if request.method == 'POST':
        art.user.add(user_)
    return redirect('article', slug_category, slug_article)


def add_word_to_dictionary(request, slug_article, slug_category):
    art = get_object_or_404(Article, slug_article=slug_article)
    user_ = request.user
    if request.method == 'POST':
        word_ = request.POST.get('word')
        try:
            word_add = Dictionary.objects.get(word=word_)
        except Exception as e:
            word_add = Dictionary.objects.create(word=word_)

        word_add.user.add(user_)

        return redirect('article', slug_category, slug_article)
    else:
        form = DictionaryForm()

    return render(
        request,
        'add_word.html',
        context={'article': art,
                 'form': form,
                 'slug_category': slug_category,
                 'slug_article': slug_article,
                 })

def delete_favorite_article(request:HttpResponse, slug_article):
    user_ = request.user
    article = get_object_or_404(Article, slug_article=slug_article)
    article.user.remove(user_)
    return redirect('my_page')


def get_favorite_article(request):
    user_ = request.user
    favorite_art = [name for name in user_.favorite_art.all()]
    words = [word for word in user_.words.all().order_by('word')]

    return render(
        request,
        'my_page.html',
        context={'favorite_art': favorite_art,
                 'user': user_,
                 'words': words
                 }
    )


def _translate(word, language):
    word_for_translation = word.word
    abbr = language.abbreviation
    translator = Translator()
    translated_word = translator.translate(word_for_translation, dest=abbr)
    translated_word = translated_word.text
    Translation.objects.create(word=word,
                               translation=translated_word,
                               language=language)


def translate_word(request, pk):
    user_ = request.user
    word_ = get_object_or_404(Dictionary, pk=pk)
    word_for_translation = word_.word
    form_post = LanguageForm(request.POST or None)
    translated_word, lang = '', ''
    abbr = ''
    if request.method == 'POST' and form_post.is_valid():
        lang = form_post.cleaned_data.get('language')
        lang_object = Language.objects.get(language=lang)
        translated_word = word_.translations.filter(language=lang_object)
        if not translated_word:
            _translate(word_, lang_object)
        translated_word = word_.translations.get(language=lang_object)

    return render(
        request,
        'translation.html',
        context={'word': word_for_translation,
                 'translated_word': translated_word,
                 'lang': lang,
                 'form_post': form_post,
                 'abbr': abbr
                 }
    )


class VerificationTest:
    def __init__(self,  user=None, language=None, status=None):
        self.status = status
        self.user = user
        self.language = language

    TEST_WORDS = {}
    ANSWER_TEST = []

    def _get_options(self, word_, options, words):
        if not word_.translations.filter(language=self.language):
            _translate(word_, self.language)
        translation_ = word_.translations.get(language=self.language)
        return translation_



    def get_question_of_words(self):
        dict_ = Dictionary.objects.filter(user=self.user)
        all_words = [word for word in dict_]
        count = len(all_words)
        words, right_otions = {}, []
        num, amount = 0, 5
        if count < 5:
            amount = count
        for _ in range(amount):
            numbers = []
            number = random.randrange(count)
            numbers.append(number)
            word = all_words[number]
            options = []
            option = self._get_options(word, options, words)
            options.append(option)
            right_otions.append(option)
            while len(options) < 3:
                number = random.randrange(count)
                if number not in numbers:
                    numbers.append(number)
                    word_ = all_words[number]
                    option = self._get_options(word_, options, words)
                    options.append(option)
            random.shuffle(options)
            words[word] = options
            num += 1
        global TEST_WORDS
        global ANSWER_TEST
        TEST_WORDS = words
        ANSWER_TEST = right_otions

        return words


    def get_result(self, request):
        wrong = 0
        correct = 0
        total = 0
        answers = []
        words = []
        x = []
        for w in TEST_WORDS.keys():
            words.append(w.word)
            answer = request.POST.get(w.word)
            answers.append(answer)
            j = ANSWER_TEST[total].translation
            x.append(j)
            if j == answer:
                correct += 1
            else:
                wrong += 1
            total += 1
        return wrong, correct, total, x


def get_test(request: HttpResponse):
    if request.method == 'POST':
        result = VerificationTest()
        result = result.get_result(request)
        wrong, correct, total, x = result

    return render(
        request,
        'result.html',
        context={'wrong': wrong,
                 'correct': correct,
                 'total': total,
                 'x': x}
    )


def get_test_language(request: HttpResponse):
    # form_language = LanguageForm()
    form_language = LanguageForm(request.POST or None)

    if request.method == 'POST' and form_language.is_valid():
        amount_dict_ = Dictionary.objects.filter(user=request.user).count()
        if amount_dict_ < 3:
            return redirect('my_page')
        lang = form_language.cleaned_data.get('language')
        lang_object = Language.objects.get(language=lang)
        user = request.user
        words = VerificationTest(user=user, language=lang)
        words = words.get_question_of_words()

        return render(request,
                      'test.html',
                      context={'language': lang_object,
                               'words': words})

    return render(request,
                  'test_language.html',
                  context={'form': form_language}
                  )












