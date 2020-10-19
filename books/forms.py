from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import Book


class BookAddForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class BookSearchForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=False,
        label="Tytuł",
        widget=forms.TextInput(attrs={"placeholder": "Tytuł książki"}),
    )
    author = forms.CharField(
        max_length=200,
        required=False,
        label="Autor",
        widget=forms.TextInput(attrs={"placeholder": "Autor książki"}),
    )
    language = forms.CharField(
        max_length=3,
        required=False,
        label="Język książki (skrót)",
        widget=forms.TextInput(attrs={"placeholder": "pl, en, de"}),
    )
    date_from = forms.IntegerField(
        min_value=1900,
        required=False,
        label="Rok publikacji od:",
        widget=forms.NumberInput(attrs={"placeholder": "Rok publikacji"}),
    )
    date_to = forms.IntegerField(
        min_value=1901,
        max_value=int(timezone.now().year),
        required=False,
        label="do",
        widget=forms.NumberInput(attrs={"placeholder": "Rok publikacji"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        if not date_to:
            date_to = int(timezone.now().year)

        if not date_from:
            date_from = 1901

        if date_to <= date_from:
            raise forms.ValidationError(
                _("End date should be greater than start date.")
            )


class GoogleBooksForm(forms.Form):
    key_word = forms.CharField(
        max_length=50,
        label="Proszę podać słowa kluczowe dla książek do zaimportowania:",
    )
    in_title = forms.CharField(
        max_length=50,
        label="Tytuł książki (opcjonalnie):",
        widget=forms.TextInput,
        required=False,
    )
    in_author = forms.CharField(
        max_length=50,
        label="Autor książki (opcjonalnie):",
        widget=forms.TextInput,
        required=False,
    )
