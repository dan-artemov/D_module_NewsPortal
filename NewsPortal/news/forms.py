from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'post_header',
            'post_text',
            'categories',
            # 'post_type'
        ]
    def clean_post_header(self):
        name = self.cleaned_data["post_header"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'post_header',
            'post_text',
            'categories',
            # 'post_type'
        ]
    def clean_post_header(self):
        name = self.cleaned_data["post_header"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name




