import requests
import re

from .models import Book

APIkey = 'AIzaSyAEvQDlkulKnf_G4qWSguMJqlrPHcOSVgQ'

google_books_url = 'https://www.googleapis.com/books/v1/volumes'


def fetch_book_data(q):
    if isinstance(q, str):
        param = {'q': q, 'key': APIkey}
        response = requests.get(google_books_url, params=param).json()
    else:
        return False

    for book in response['items']:
        published_date = book['volumeInfo']['publishedDate'] if 'publishedDate' in book['volumeInfo'] else ''
        page_num = book['volumeInfo']['pageCount'] if 'pageCount' in book['volumeInfo'] else 1
        link_to_cover = book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else ''
        author= '\n'.join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else 'Brak autora'

        new_book = Book.objects.get_or_create(
            title=book['volumeInfo']['title'],
            author=author,
            isbn=isbn_check(book['volumeInfo']['industryIdentifiers']),
            publication_date=publish_date_check(published_date),
            page_num=page_num,
            book_language=book['volumeInfo']['language'],
            link_to_cover=link_to_cover,
        )
    book_count = response['totalItems']

    return book_count


def publish_date_check(published_date):
    if not published_date:
        return ''
    year = re.search(r'\d{4}', published_date)
    return year.group()


def isbn_check(isbn_list):
    result = ''
    for isbn in isbn_list:
        if 'ISBN_13' in isbn.values():
            result = isbn['identifier']
            return result
        elif 'ISBN_10' in isbn.values():
            result = isbn['identifier']
        elif not result:
            result = 'Inny rodzaj identyfikatora'

    return result
