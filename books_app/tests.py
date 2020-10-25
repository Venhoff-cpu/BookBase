from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from books_app.forms import BookAddForm, BookSearchForm, GoogleBooksForm
from books_app.models import Book


def create_book_1():
    Book.objects.create(
        author="J.R.R. Tolkien",
        title="Hobbit",
        isbn=1234567891012,
        publication_date=2007,
        page_num=155,
        link_to_cover="https://getbootstrap.com/",
        book_language="pl",
    )


def create_book_2():
    Book.objects.create(
        author="J.R.R. Tolkien",
        title="Lord of the rings",
        isbn=1234567892222,
        publication_date=2007,
        page_num=155,
        link_to_cover="https://getbootstrap.com/",
        book_language="pl",
    )


class GetViewsTest(TestCase):
    def setUp(self):
        create_book_1()

    def test_index(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_book_list(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_add(self):
        url = reverse("book-add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_edit(self):
        book = Book.objects.get(title="Hobbit")
        url = reverse("book-edit", kwargs={"pk": book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_add_api(self):
        url = reverse("book-add-google")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_api(self):
        url = reverse("book-api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class BookFormAddTest(TestCase):
    def setUp(self):
        create_book_1()
        self.url = reverse("book-add")

    def test_form_correct(self):
        response = self.client.post(
            self.url,
            {
                "author": "J.R.R. Tolkien",
                "title": "Hobbit: tam i z powrotem",
                "isbn": 1234567891022,
                "publication_date": 2002,
                "page_num": 120,
                "link_to_cover": "https://getbootstrap.com/",
                "book_language": "pl",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.all().count(), 2)

    def test_form_validation(self):
        form_params = {
            "author": "J.R.R. Tolkien",
            "title": "Hobbit: tam i z powrotem",
            "isbn": 1234567891012,
            "publication_date": 0,
            "page_num": "aaa",
            "link_to_cover": "asss",
            "book_language": "wdawa",
        }
        form = BookAddForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["isbn"][0],
            "Istnieje już Ksiąźka z tą wartością pola ISBN.",
        )
        self.assertEqual(
            form.errors["publication_date"][0],
            "Upewnij się, że ta wartość jest większa lub równa 1900.",
        )
        self.assertEqual(form.errors["page_num"][0], "Wpisz liczbę całkowitą.")
        self.assertEqual(
            form.errors["link_to_cover"][0], "Wprowadź poprawny adres URL."
        )
        self.assertEqual(
            form.errors["book_language"][0],
            "Upewnij się, że ta wartość ma co najwyżej 3 znaki "
            "(obecnie ma 5).",
        )


class BookSearchFormTest(TestCase):
    def setUp(self):
        create_book_1()
        create_book_2()
        self.url = reverse("book-list")

    def test_form_validation(self):
        form_params = {
            "author": "J.R.R. Tolkien",
            "title": "Hobbit",
            "date_to": 2021,
            "date_from": 0,
            "page_num": "aaa",
            "language": "wdawa",
        }
        form = BookSearchForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["date_to"][0],
            "Upewnij się, że ta wartość jest mniejsza lub równa 2020.",
        )
        self.assertEqual(
            form.errors["date_from"][0],
            "Upewnij się, że ta wartość jest większa lub równa 1900.",
        )
        self.assertEqual(
            form.errors["language"][0],
            "Upewnij się, że ta wartość ma co najwyżej 3 znaki "
            "(obecnie ma 5).",
        )

    def test_form_get(self):
        form_params = {
            "author": "J.R.R. Tolkien",
            "title": "Lord",
            "date_to": 2008,
            "date_from": 2006,
            "page_num": 155,
            "language": "pl",
        }
        response = self.client.get(self.url, form_params)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["object_list"],
            Book.objects.filter(title="Lord of the rings"),
            transform=lambda x: x,
        )


class BookGoogleApiTest(TestCase):
    def setUp(self):
        self.url = reverse("book-add-google")
        self.form_params = {
            "key_word": "Hobbit",
            "in_title": "",
            "in_author": "",
        }

    def test_google_form_succses(self):
        form = GoogleBooksForm(self.form_params)
        self.assertTrue(form.is_valid())

    def test_google_form_fail(self):
        form_params = {
            "key_word": "",
            "in_title": "a" * 51,
            "in_author": "a" * 51,
        }
        form = GoogleBooksForm(form_params)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["key_word"][0],
            "To pole jest wymagane.")
        self.assertEqual(
            form.errors["in_title"][0],
            "Upewnij się, że ta wartość ma co najwyżej 50 znaków "
            "(obecnie ma 51).",
        )
        self.assertEqual(
            form.errors["in_author"][0],
            "Upewnij się, że ta wartość ma co najwyżej 50 znaków "
            "(obecnie ma 51).",
        )

    def test_get_google_books(self):
        response = self.client.post(self.url, self.form_params)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.all().count(), 10)


class BookEditTest(TestCase):
    def setUp(self):
        create_book_1()
        create_book_2()
        self.book = Book.objects.get(title="Hobbit")
        self.url = reverse("book-edit", kwargs={"pk": self.book.id})

    def test_form_success(self):
        form_params = {
            "author": "J.R.R. Tolkien",
            "title": "Hobbit: Czyli tam i z powrotem",
            "publication_date": 1999,
            "isbn": "1234567891221",
            "page_num": 200,
            "book_language": "en",
            "link_to_cover": "https://getbootstrap.com/test",
        }

        response = self.client.post(self.url, form_params)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Book.objects.filter(title="Hobbit"))
        self.assertTrue(
            Book.objects.filter(title="Hobbit: Czyli tam i z powrotem")
        )

        self.book.refresh_from_db()

        self.assertEqual(self.book.publication_date, 1999)
        self.assertEqual(self.book.isbn, "1234567891221")
        self.assertEqual(self.book.page_num, 200)
        self.assertEqual(self.book.book_language, "en")
        self.assertEqual(
            self.book.link_to_cover, "https://getbootstrap.com/test"
        )

    def test_form_validation(self):
        form_params = {
            "author": "J.R.R. Tolkien",
            "title": "Hobbit: tam i z powrotem",
            "isbn": 1234567892222,
            "publication_date": 0,
            "page_num": "aaa",
            "link_to_cover": "asss",
            "book_language": "wdawa",
        }

        response = self.client.post(self.url, form_params)
        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["isbn"][0],
            "Istnieje już Ksiąźka z tą wartością pola ISBN.",
        )
        self.assertEqual(
            form.errors["publication_date"][0],
            "Upewnij się, że ta wartość jest większa lub równa 1900.",
        )
        self.assertEqual(form.errors["page_num"][0], "Wpisz liczbę całkowitą.")
        self.assertEqual(
            form.errors["link_to_cover"][0], "Wprowadź poprawny adres URL."
        )
        self.assertEqual(
            form.errors["book_language"][0],
            "Upewnij się, że ta wartość ma co najwyżej 3 znaki "
            "(obecnie ma 5).",
        )


class ApiViewTest(APITestCase):
    def setUp(self):
        form_params = {
            "key_word": "Hobbit",
            "in_title": "",
            "in_author": "",
        }
        self.client.post(reverse("book-add-google"), form_params)
        self.url = reverse("book-api")
        create_book_1()

    def test_api_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["count"], 11)

    def test_api_get_query(self):
        form_params = {
            "author": "J.R.R. Tolkien",
            "title": "Hobbit",
            "publication_date__lte": 2008,
            "publication_date__gte": 2006,
            "language": "pl",
        }

        response = self.client.get(self.url, form_params, format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["count"], 1)

        self.assertEqual(data["results"][0]["publication_date"], 2007)
        self.assertEqual(data["results"][0]["title"], "Hobbit")
        self.assertEqual(data["results"][0]["isbn"], "1234567891012")
