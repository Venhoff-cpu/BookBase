# Generated by Django 3.1.2 on 2020-10-25 14:01

import books_app.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200, verbose_name='author')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('publication_date', models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(limit_value='1900-01-01', message='Książka nie może mieć daty'), django.core.validators.MaxValueValidator(limit_value=books_app.models.current_date, message='Książka nie może być z przyszłości.')], verbose_name='Publication date')),
                ('isbn', models.CharField(blank=True, default=None, max_length=256, null=True, unique=True, validators=[books_app.models.isbn_validator], verbose_name='ISBN')),
                ('page_num', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Liczba stron nie może byc równa lub mniejsza od 0'), django.core.validators.MaxValueValidator(limit_value=1000)])),
                ('link_to_cover', models.URLField(blank=True, help_text='Pełny link zaczynający się od http:// lub https://', null=True, verbose_name='Link to book cover')),
                ('book_language', models.CharField(help_text='Prosze podać skrót (zgodnie z ISO) języka w jakim napisana jest książka.', max_length=3)),
            ],
            options={
                'verbose_name': 'Ksiąźka',
                'verbose_name_plural': 'Ksiąźki',
                'ordering': ['title', 'publication_date'],
            },
        ),
    ]
