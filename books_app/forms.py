import datetime

from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import Book


class BookAddForm(ModelForm):
    publication_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

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
    date_from = forms.DateField(
        required=False,
        label="Rok publikacji od:",
        widget=forms.DateInput(attrs={"placeholder": "Rok publikacji", "type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        label="do",
        widget=forms.DateInput(attrs={"placeholder": "Rok publikacji", "type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        if not date_to:
            date_to = timezone.now().date()

        if not date_from:
            date_from = datetime.date(1900, 1, 1)

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
