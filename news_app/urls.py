from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('signup', views.sign_up, name='signup'),
    path('<slug:slug_category>', views.get_article, name='category'),
    path('<slug:slug_category>/<slug:slug_article>', views.get_story_and_comments, name='article'),
    path('<slug:slug_category>/<slug:slug_article>/create_comment', views.add_comment, name='create_comment'),
    path('<slug:slug_category>/<slug:slug_article>/delete/<int:pk>', views.delete_comment, name='del_comment'),
    path('<slug:slug_category>/<slug:slug_article>/update/<int:pk>', views.update_comment, name='update_comment'),
    path('<slug:slug_category>/<slug:slug_article>/like_comment/<int:pk>', views.like_comment, name='likes_comment'),
    path('<slug:slug_category>/<slug:slug_article>/like_article', views.like_article, name='likes_article'),

    path('accounts/', include('django.contrib.auth.urls')),


]

