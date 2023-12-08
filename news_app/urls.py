from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("signup", views.sign_up, name="signup"),
    path("my_page", views.get_favorite_article, name="my_page"),
    path(
        "my_page/delete/<slug:slug_article>",
        views.delete_favorite_article,
        name="delete_favorite_article",
    ),
    path("my_page/test_language", views.get_test_language, name="test_language"),
    path("my_page/result", views.get_test, name="result_test"),
    path("my_page/translate/<int:pk>", views.translate_word, name="translation"),
    path("<slug:slug_category>", views.get_article, name="category"),
    path(
        "<slug:slug_category>/<slug:slug_article>",
        views.get_story_and_comments,
        name="article",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/create_comment",
        views.add_comment,
        name="create_comment",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/delete/<int:pk>",
        views.delete_comment,
        name="del_comment",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/update/<int:pk>",
        views.update_comment,
        name="update_comment",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/like_comment/<int:pk>",
        views.like_comment,
        name="likes_comment",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/like_article",
        views.like_article,
        name="likes_article",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/dislike_article",
        views.dislike_article,
        name="dislikes_article",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/add_favorite_art",
        views.add_favorite_article,
        name="add_favorite_art",
    ),
    path(
        "<slug:slug_category>/<slug:slug_article>/add_word",
        views.add_word_to_dictionary,
        name="add_word_to_dictionary",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]
