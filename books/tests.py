import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from django.core.exceptions import ValidationError

from books.models import Book
from books.forms import BookAddForm, BookSearchForm, GoogleBooksForm


class GetViewsTest(TestCase):
    def setUp(self):
        new_book = Book.objects.create(
            author='J.R.R. Tolkien',
            title='Hobbit',
            isbn=1234567891012,
            publication_date=2007,
            page_num=155,
            link_to_cover='https://getbootstrap.com/',
            book_language='pl',
        )
        new_book.save()

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_add(self):
        url = reverse('book-add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_api(self):
        url = reverse('book-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_edit(self):
        book = Book.objects.get(title='Hobbit')
        url = reverse('book-edit', kwargs={'pk': book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_add_api(self):
        url = reverse('book-add-google')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_api(self):
        url = reverse('book-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class BookFormAddTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            author='J.R.R. Tolkien',
            title='Hobbit',
            isbn=1234567891012,
            publication_date=2007,
            page_num=155,
            link_to_cover='https://getbootstrap.com/',
            book_language='pl',
        )
        self.url = reverse('book-add')

    def test_correct(self):
        response = self.client.post(
            self.url,
            {'author': 'J.R.R. Tolkien',
             'title': 'Hobbit: tam i z powrotem',
             'isbn': 1234567891022,
             'publication_date': 2002,
             'page_num': 120,
             'link_to_cover': 'https://getbootstrap.com/',
             'book_language': 'pl'})
        self.assertTrue(response.status_code, 302)
        self.assertEqual(Book.objects.all().count(), 2)

    def test_validation(self):
        form_params = {'author': 'J.R.R. Tolkien',
                       'title': 'Hobbit: tam i z powrotem',
                       'isbn': 1234567891012,
                       'publication_date': 0,
                       'page_num': 'aaa',
                       'link_to_cover': 'asss',
                       'book_language': 'wdawa'}
        form = BookAddForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['isbn'][0], 'Invalid ISBN: already exists')
        self.assertEqual(form.errors['publication_date'][0], 'Upewnij się, że ta wartość jest większa lub równa 1900.')
        self.assertEqual(form.errors['page_num'][0], 'Wpisz liczbę całkowitą.')
        self.assertEqual(form.errors['link_to_cover'][0], 'Wprowadź poprawny adres URL.')
        self.assertEqual(form.errors['book_language'][0],
                         'Upewnij się, że ta wartość ma co najwyżej 3 znaki (obecnie ma 5).')
