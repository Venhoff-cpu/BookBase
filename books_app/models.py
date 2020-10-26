from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import datetime


def current_date():
    return timezone.now().date()


future_date = MaxValueValidator(
    limit_value=current_date,
    message="Książka nie może być z przyszłości.",
)
past_date = MinValueValidator(
    limit_value=datetime.date(1900, 1, 1),
    message="Zbyt odległa data",
)


def isbn_validator(raw_isbn):
    """ Check string is a valid ISBN number"""
    isbn_to_check = raw_isbn.replace("-", "").replace(" ", "")

    if not isinstance(isbn_to_check, str):
        raise ValidationError(_("Invalid ISBN: Not a string"))

    if isbn_to_check == "Inny rodzaj identyfikatora":
        return True

    if len(isbn_to_check) != 10 and len(isbn_to_check) != 13:
        raise ValidationError(_("Invalid ISBN: Wrong length"))

    if isbn_to_check != isbn_to_check.upper():
        raise ValidationError(_("Invalid ISBN: Only upper case allowed"))

    return True


class Book(models.Model):
    author = models.CharField(
        max_length=200,
        verbose_name=_("author"),
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("title"),
    )
    publication_date = models.DateField(
        blank=True,
        null=True,
        validators=[
            past_date,
            future_date,
        ],
        verbose_name=_("Publication date"),
    )
    isbn = models.CharField(
        unique=True,
        blank=True,
        null=True,
        default=None,
        max_length=256,
        validators=[isbn_validator],
        verbose_name=_("ISBN"),
    )
    page_num = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Liczba stron nie może byc równa lub mniejsza od 0",
            ),
            MaxValueValidator(limit_value=1000),
        ]
    )
    link_to_cover = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Link to book cover"),
        help_text="Pełny link zaczynający się od http:// lub https://",
    )
    book_language = models.CharField(
        max_length=3,
        help_text="Prosze podać skrót (zgodnie z ISO) "
                  "języka w jakim napisana jest książka.",
    )

    def __str__(self):
        return f'{self.author} "{self.title}"'

    class Meta:
        verbose_name = "Ksiąźka"
        verbose_name_plural = "Ksiąźki"
        ordering = [
            "title",
            "publication_date",
        ]
