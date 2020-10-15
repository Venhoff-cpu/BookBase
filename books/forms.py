from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .models import Book


class BookAddForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False, label='Tytuł')
    author = forms.CharField(max_length=200, required=False, label='Autor')
    language = forms.CharField(
        max_length=2,
        required=False,
        label='Język',
        help_text='Językyk prosze podać zgodnie z skrótami ISO')
    date_from = forms.IntegerField(min_value=1900, required=False, label='Rok publikacji od:')
    date_to = forms.IntegerField(
        min_value=1901,
        max_value=int(timezone.now().year),
        required=False,
        label='Do',
        help_text='Wartości należy podać jako rok publikacji')

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        if not date_to:
            date_to = int(timezone.now().year)

        if not date_from:
            date_from = 1901

        if date_to <= date_from:
            raise forms.ValidationError(_("End date should be greater than start date."))


class GoogleBooksForm(forms.Form):
    key_word = forms.CharField(max_length=50, label='Proszę podać słowa kluczowe dla książek do zaimportowania:')
    in_title = forms.CharField(
        max_length=50,
        label='Tytuł książki (opcjonalnie):',
        widget=forms.TextInput, required=False)
    in_author = forms.CharField(
        max_length=50,
        label='Autor książki (opcjonalnie):',
        widget=forms.TextInput, required=False)
