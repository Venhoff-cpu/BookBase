from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from django.utils import timezone


def today_date():
    return timezone.now().date()


future_date = MaxValueValidator(
    limit_value=today_date(),
    message="Książka nie może być z przyszłości.",
)


def ISBN_validator(raw_isbn):
    """ Check string is a valid ISBN number"""
    isbn_to_check = raw_isbn.replace('-', '').replace(' ', '')

    if not isinstance(isbn_to_check, str):
        raise ValidationError(_(u'Invalid ISBN: Not a string'))

    if len(isbn_to_check) != 10 and len(isbn_to_check) != 13:
        raise ValidationError(_(u'Invalid ISBN: Wrong length'))

    if isbn_to_check != isbn_to_check.upper():
        raise ValidationError(_(u'Invalid ISBN: Only upper case allowed'))

    return True


class Book(models.Model):
    author = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("author"),)
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("title"),)
    publication_date = models.DateField(
        validators=[future_date],
        verbose_name=_('Publication date'))
    isbn = models.CharField(
        max_length=17,
        unique=True,
        validators=[ISBN_validator],
        verbose_name=_('ISBN'),)
    page_num = models.IntegerField(
        max_length=1000,
        validators=[MinValueValidator(limit_value=1, message='Liczba stron nie może byc równa lub mniejsza od 0')])
    link_to_cover = models.URLField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name=_('Link to book cover')
    )

    def __str__(self):
        return f'{self.author} "{self.title}"'
