# Generated by Django 3.1.2 on 2020-10-15 13:28

import django.core.validators
from django.db import migrations, models

import books.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "author",
                    models.CharField(max_length=200, verbose_name="author"),
                ),
                (
                    "title",
                    models.CharField(max_length=200, verbose_name="title"),
                ),
                (
                    "publication_date",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(2020)
                        ],
                        verbose_name="Publication date",
                    ),
                ),
                (
                    "isbn",
                    models.CharField(
                        max_length=17,
                        validators=[books.models.ISBN_validator],
                        verbose_name="ISBN",
                    ),
                ),
                (
                    "page_num",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1,
                                message="Liczba stron nie może byc równa lub mniejsza od 0",
                            ),
                            django.core.validators.MaxValueValidator(
                                limit_value=1000
                            ),
                        ]
                    ),
                ),
                (
                    "link_to_cover",
                    models.URLField(
                        blank=True,
                        unique=True,
                        verbose_name="Link to book cover",
                    ),
                ),
                (
                    "book_language",
                    models.CharField(
                        help_text="Prosze podać język w jakim napisana jest książka.",
                        max_length=200,
                    ),
                ),
            ],
            options={
                "verbose_name": "Ksiąźka",
                "verbose_name_plural": "Ksiąźki",
                "ordering": ["title", "publication_date"],
            },
        ),
    ]