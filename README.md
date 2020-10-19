# BookBase
Zadanie rekrutacyjne - STX next
Strona intenetowa napsiana w Django pozwalajaca na dodawania i przeglądanie książek.
Książki mogą być dodawane bezpośrednio przez aplikację, jak i poprzez Google Books API.

Aplikacja udostępnia server REST API - tylko pobieranie i wyszukiwanie danych.

## Wymagania

Aby zainstalować wszystkie użyte pakiety użyj następującej w wierszu poleceń w terminalu
podczas gdy twoje wirtualne środowisko dla projektu jest aktywne:
```python
$ pip install -r requirements.txt
```

## Konfiguracja 

Projekt używa django-environ.
W celu konfiguracji usuń z pliku ```.env.sample``` końcówkę sample i uzupełnij plik swojimi danymi.
```
DEBUG=True
SECRET_KEY=<your-secret-key>
DATABASE_URL=postgres://user:password@host:port/production_db
GOOGLE_BOOKS_API_KEY=<your-google-books-api-key>
```

W projekcie użyto systemu bazodanowego Postgresql.
```heroku.py``` jest plikiem konfiguracyjnym dla Heroku.

## Używanie API

W celu pobrania książek za pomocą usługi REST API należy wysłać zapytanie do:
```
nazwastrony.com/api/book-list/
```
Zapytanie zwróci obiekt typu JSON, w którym pod kluczem ```items``` zwrócone zostaną dane na temat książek znajdujących 
się w bazie.

W celu wyszukania konkretnej książki można w url przekazać query strings.
API obsługuje następujące parametry wyszukiwania:
- ```title``` - przeszukuje bazę pod kontem tytułu książki.
- ```author``` - przeszukuje bazę pod kontem autora książki.
- ```book_language``` - przeszukuje bazę po jeżyku książki. Parametr tu przekazany powninen mieć formę skróconej
reprezentacji danego języka np. Polski - pl, Niemiecki - de itd.
- ```publication_date__gte``` i ```publication_date__lte``` - przeszukuje bazę pod kontem daty publikacji książki.
gte oznacza datę po której książka została wydana, a lte, datę przed którą książka została wydana. 
Dla tych paranmetrów należy podawać tylko rok.

Parametry wyszukiwania łączą się ze sobą. Pozostawienie parametru pustego uznaje się za pominięcie danego kryterium.

Przykład: Chcemy wyszukać książkę o tytule 'Hobbit', autorze: ' Tolkien', języku książki: 'Angielskim', 
wydanej w latach między 1990, a 2005.

Przy takich założeniach zapytanie do API, będzie wygładało następująco:
```python
url = 'api/book-list/?author=Tolkien&title=Hobbit&book_language=en&publication_date__gte=1990&publication_date__lte=2005'
```
