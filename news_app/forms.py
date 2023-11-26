
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from news_app.models import Comment, Article, Dictionary, Language




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

levels = ((1, 'Beginner'),
          (2, 'Intermediate'),
          (3, 'Advanced'),
          (4, 'All')
          )
class LevelForm(forms.Form):
    levels = forms.TypedChoiceField(label='sort', choices=levels,
                                       coerce=int)


class DictionaryForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ('word',)


class LanguageForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.all())

    class Meta:
        model = Language
        fields = ('language',)

class TranslationForm(forms.Form):
    translation = forms.CharField()


# class OptionForm(forms.Form):
#     translations = forms.TypedChoiceField(label='options', choices=options,
#                                     coerce=int)




#
# language =((1, 'belarusian','be'),
#            (2, 'german', 'de'),
#            (3, 'polish', 'pl'),
#            (4, 'french', 'fr'),
#            (5, 'italian', 'it'),
#            (6, 'spanish', 'es'),
#            (7, 'ukrainian', 'uk'),
#            (8, 'chinese (simplified)', 'zh-cn'),
#            (9, 'russian', 'ru'),
#            (10, 'korean', 'ko')
#
# )


















# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(label='username', min_length=5, max_length=150)
#     # email = forms.EmailField(label='email')
#     password1 = forms.CharField(label='password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
#
#     def username_clean(self):
#         username = self.cleaned_data['username'].lower()
#         new = User.objects.filter(username=username)
#         if new.count():
#             raise ValidationError("User Already Exist")
#         return username

    # def email_clean(self):
    #     email = self.cleaned_data['email'].lower()
    #     new = User.objects.filter(email=email)
    #     if new.count():
    #         raise ValidationError(" Email Already Exist")
    #     return email

    # def clean_password2(self):
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Password don't match")
    #     return password2
    #
    # def save(self, commit=True):
    #     user = User.objects.create_user(
    #         self.cleaned_data['username'],
    #         self.cleaned_data['email'],
    #         self.cleaned_data['password1']
    #     )
    #     return user
    #

