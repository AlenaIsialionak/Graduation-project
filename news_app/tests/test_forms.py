from django.test import TestCase
from news_app.forms import CommentForm


class TestForms(TestCase):

    def level_form_valid(self):
        form = CommentForm(
            data={
                'content': 'Beginner'
            }
        )

        self.assertTrue(form.is_valid())


    def test_form_no_data(self):
        form = CommentForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
