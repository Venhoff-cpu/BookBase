from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Book


class BookAddForm(ModelForm):

    class Meta:
        model = Book


class BookSearchForm(forms.Form):
    pass
