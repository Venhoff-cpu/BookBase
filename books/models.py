from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from django.utils import timezone


def current_year():
    return timezone.now().year


future_date = MaxValueValidator(
    limit_value=current_year(),
    message="Książka nie może być z przyszłości.",
)


def ISBN_validator(raw_isbn):
    """ Check string is a valid ISBN number"""
    isbn_to_check = raw_isbn.replace('-', '').replace(' ', '')

    if not isinstance(isbn_to_check, str):
        raise ValidationError(_(u'Invalid ISBN: Not a string'))

    if isbn_to_check == 'Inny rodzaj identyfikatora':
        return True

    if len(isbn_to_check) != 10 and len(isbn_to_check) != 13:
        raise ValidationError(_(u'Invalid ISBN: Wrong length'))

    if isbn_to_check != isbn_to_check.upper():
        raise ValidationError(_(u'Invalid ISBN: Only upper case allowed'))

    return True


class Book(models.Model):
    author = models.CharField(
        max_length=200,
        verbose_name=_("author"),)
    title = models.CharField(
        max_length=200,
        verbose_name=_("title"),)
    publication_date = models.IntegerField(
        blank=True,
        validators=[MaxValueValidator(current_year())],
        verbose_name=_('Publication date'),)
    isbn = models.CharField(
        max_length=256,
        validators=[ISBN_validator],
        verbose_name=_('ISBN'),)
    page_num = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=1, message='Liczba stron nie może byc równa lub mniejsza od 0'),
            MaxValueValidator(limit_value=1000)])
    link_to_cover = models.URLField(
        blank=True,
        verbose_name=_('Link to book cover'),
        help_text='Pełny link zaczynający się od http:// lub https://',
    )
    book_language = models.CharField(
        max_length=200,
        help_text='Prosze podać skrót (zgodnie z ISO) języka w jakim napisana jest książka.')

    def __str__(self):
        return f'{self.author} "{self.title}"'

    class Meta:
        verbose_name = "Ksiąźka"
        verbose_name_plural = "Ksiąźki"
        ordering = [
            "title",
            "publication_date",
        ]
