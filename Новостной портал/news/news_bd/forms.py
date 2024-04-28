from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class Newsform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author','category', 'title', 'text' ]
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is not None and len(title) < 20:
            raise ValidationError({'title': 'Заголовок новости не может быть меньше 30 символов'})
        text = cleaned_data.get('text')
        if text is not None and len(text) < 50:
            raise ValidationError({'text': 'Текст новости не может быть меньше 50 символов'})


class Articleform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author','category', 'title', 'text' ]
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title is not None and len(title) < 20:
            raise ValidationError({'title': 'Заголовок статьи не может быть меньше 30 символов'})
        text = cleaned_data.get('text')
        if text is not None and len(text) < 100:
            raise ValidationError({'text': 'Текст статьи не может быть меньше 100 символов'})

