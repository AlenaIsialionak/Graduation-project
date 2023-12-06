from django.test import SimpleTestCase
from django.urls import reverse, resolve
from news_app.views import get_test_language, get_favorite_article


class TestUrls(SimpleTestCase):

    def test_language_of_test_resolves(self):
        url = reverse('my_page')
        print(resolve(url))
        self.assertEquals(resolve(url).func, get_favorite_article)


    def test_my_page_url_is_resolved(self):
        url = reverse('test_language')
        print(resolve(url))
        self.assertEquals(resolve(url).func, get_test_language)

