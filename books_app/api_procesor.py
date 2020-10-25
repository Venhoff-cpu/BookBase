import re

import requests
import datetime

from .models import Book
from Project_BookBase.settings.base import GOOGLE_BOOKS_API_KEY

APIkey = GOOGLE_BOOKS_API_KEY

google_books_url = "https://www.googleapis.com/books/v1/volumes"


def fetch_book_data(q):
    if isinstance(q, str):
        param = {"q": q, "key": APIkey}
        response = requests.get(google_books_url, params=param).json()
    else:
        return False

    return response


def process_book_data(response):
    book_objs = []
    for book in response["items"]:
        published_date = (
            book["volumeInfo"]["publishedDate"]
            if "publishedDate" in book["volumeInfo"].keys()
            else None
        )
        page_num = (
            book["volumeInfo"]["pageCount"]
            if "pageCount" in book["volumeInfo"].keys()
            else None
        )
        link_to_cover = (
            book["volumeInfo"]["imageLinks"]["thumbnail"]
            if "imageLinks" in book["volumeInfo"].keys()
            else None
        )
        author = (
            ", ".join(book["volumeInfo"]["authors"])
            if "authors" in book["volumeInfo"].keys()
            else ""
        )
        isbn = isbn_check(book["volumeInfo"]["industryIdentifiers"])
        if Book.objects.filter(isbn=isbn) and isbn:
            continue

        obj = Book(
            title=book["volumeInfo"]["title"],
            author=author,
            isbn=isbn_check(book["volumeInfo"]["industryIdentifiers"]),
            publication_date=publish_date_check(published_date),
            page_num=page_num,
            book_language=book["volumeInfo"]["language"],
            link_to_cover=link_to_cover,
        )

        book_objs.append(obj)

    return book_objs


def publish_date_check(published_date):
    if not published_date:
        return None
    try:
        datetime.datetime.strptime(published_date, '%Y-%m-%d')
        result = published_date
    except ValueError:
        if re.search(r"\d{4}-\d{2}", published_date):
            result = published_date + "-01"
        else:
            result = published_date + "-01-01"
    finally:
        return result


def isbn_check(isbn_list):
    result = None
    for isbn in isbn_list:
        if "ISBN_13" in isbn.values():
            result = isbn["identifier"]
            return result
        elif "ISBN_10" in isbn.values():
            result = isbn["identifier"]

    return result
