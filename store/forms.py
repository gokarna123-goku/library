from dataclasses import field

from crispy_forms.helper import FormHelper, Layout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog, Product


# REF: https://www.crunchydata.com/blog/building-a-user-registration-form-with-djangos-built-in-authentication
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')

    class Meta:
        model = User
        fields = ["first_name", "last_name","username", "password1", "password2",  "email"]

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "digital", "image", 'tag']

class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'tag']
