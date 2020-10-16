import urllib.parse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, View, UpdateView, TemplateView
from django.contrib import messages

from .models import Book
from .forms import BookAddForm, GoogleBooksForm, BookSearchForm
from .api_procesor import fetch_book_data


class LandingPage(TemplateView):
    template_name = 'book_list.html'


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 10

    def search_args(self):
        search_args = {}
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            search_args['author__icontains'] = form.cleaned_data['author']
            search_args['title__icontains'] = form.cleaned_data['title']
            search_args['book_language__icontains'] = form.cleaned_data['language']
            search_args['date_form__gte'] = form.cleaned_data['date_from']
            search_args['date_to__lte'] = form.cleaned_data['date_to']

        else:
            messages.error(self.request, 'Proszę poprawić błąd w formularzu')

        # Sprawdzenie czy nie ma pustych wartości
        search_args = {key: value for key, value in search_args.items() if value}

        return search_args

    def get_context_data(self, **kwargs):
        ctx = super(BookListView, self).get_context_data(**kwargs)
        ctx['form'] = BookSearchForm()
        return ctx

    def get_queryset(self):
        search = self.search_args()
        query = super(BookListView, self).get_queryset().filter(**search)
        return query


class BookAddView(FormView):
    form_class = BookAddForm
    fields = '__all__'
    template_name = 'book_add.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        new_book = Book.objects.create(
            author=form.cleaned_data['author'],
            title=form.cleaned_data['title'],
            isbn=form.cleaned_data['isbn'],
            publication_date=form.cleaned_data['publication_date'],
            page_num=form.cleaned_data['page_num'],
            link_to_cover=form.cleaned_data['link_to_cover'],
            book_language=form.cleaned_data['book_language'],
        )
        return super().form_valid(form)


class BookEditView(UpdateView):
    template_name = 'book_edit.html'
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('index')


class BookGoogleImportView(FormView):
    template_name = 'book_google_api.html'
    form_class = GoogleBooksForm

    def form_valid(self, form):
        key_word = form.cleaned_data['key_word']
        in_title = form.cleaned_data['in_title']
        in_author = form.cleaned_data['in_author']

        if not key_word:
            messages.error(self.request, "Słowo kluczowe jest wymagane.")
            return reverse_lazy('google-api')

        q = urllib.parse.quote(key_word)

        if in_title:
            q += f'+intitle:{urllib.parse.quote(in_title)}'

        if in_author:
            q += f'+inauthor:{urllib.parse.quote(in_author)}'

        valid = fetch_book_data(q)

        if not valid:
            messages.error(self.request, "Zapytanie nie zwróciło żdanych wartości")
            return reverse_lazy('google-api')

        messages.info(self.request, f"Pobrano {valid} pozycji do bazy danych.")

        return redirect('book-list')
