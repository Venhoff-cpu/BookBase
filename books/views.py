from django.shortcuts import render
from django.views.generic import DetailView, FormView, View

from .models import Book


class BookView(DetailView):
    model = Book
    template_name = 'books/book_list.html'
    pass


class BookAddView(FormView):
    pass


class GoogleBookAdd(View):
    pass
