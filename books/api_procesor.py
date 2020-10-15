import requests

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
        new_book = Book.objects.get_or_create(
            title=book['volumeInfo']['title'],
            author='\n'.join(book['volumeInfo']['authors']),
            isbn=isbn_check(book['volumeInfo']['industryIdentifiers']),
            publication_date=book['volumeInfo']['publishedDate'],
            page_num=book['volumeInfo']['pageCount'],
            book_language=book['volumeInfo']['language'],
            link_to_cover=book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else '',
        )
    book_count = response['totalItems']

    return book_count


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
