
from django import forms
from news_app.models import Comment, Dictionary, Language




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'class': 'comment-form'}),
        }



levels = ((1, 'Beginner'),
          (2, 'Intermediate'),
          (3, 'Advanced'),
          (4, 'All')
          )
class LevelForm(forms.Form):
    levels = forms.TypedChoiceField(choices=levels,
                                       coerce=int)


class DictionaryForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ('word',)
        widgets = {
            'word': forms.TextInput(attrs={'class': 'comment-form'}),
        }


class LanguageForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.all())

    class Meta:
        model = Language
        fields = ('language',)


class TranslationForm(forms.Form):
    translation = forms.CharField()




