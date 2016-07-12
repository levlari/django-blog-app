from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.utils.text import slugify

from .models import Article


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        # The password is already set by UserCreationForm's `save()` method.
        if commit:
            user.save()
        return user


# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ['title', 'content']

#     def __init__(self, *args, **kwargs):
#         self.author = kwargs.pop('author')
#         super(ArticleForm, self).__init__(*args, **kwargs)

#     def save(self):
#         instance = super(ArticleForm, self).save(commit=False)
#         instance.slug = slugify(instance.title)
#         instance.author = self.author
#         instance.save()
#         return instance
