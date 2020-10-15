from django.shortcuts import render, get_object_or_404
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
    paginate_by = 25

    def get_context_data(self,  **kwargs):
        ctx = super().get_context_data()
        ctx['form'] = BookSearchForm()
        return ctx

    def get_queryset(self):
        query = super(BookListView, self).get_queryset()
        print(query)
        form = BookSearchForm(self.request.GET or None)
        if form:
            if form.is_valid():
                if form.cleaned_data['author'] != '':
                    print('sprawdzam autora')
                    query = query.filter(author__icontains=form.cleaned_data['author'])
                print(query)
                if form.cleaned_data['title'] != '':
                    print(form.cleaned_data['title'])
                    print('sprawdzam title')
                    query = query.filter(title__icontains=form.cleaned_data['title'])
                print(query)
                if form.cleaned_data['language'] != '':
                    print('sprawdzam język')
                    query = query.filter(book_language__icontains=form.cleaned_data['language'])
                print(query)
                if form.cleaned_data['date_from']:
                    print('sprawdzam datę od')
                    query = query.filter(publication_date__gte=form.cleaned_data['date_from'])
                print(query)
                if form.cleaned_data['date_to']:
                    print('sprawdzam datę do')
                    query = query.filter(publication_date__lte=form.cleaned_data['date_to'])
                print(query)
            else:
                messages.error(self.request, 'Proszę poprawić błąd w formularzu')
        print(query)
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
        q = key_word

        if in_title:
            q += f'+intitle:{in_title}'

        if in_author:
            q += f'+inauthor:{in_author}'

        valid = fetch_book_data(q)

        if not valid:
            messages.error(self.request, "Zapytanie nie zwróciło żdanych wartości")
            return reverse_lazy('google-api')

        messages.info(self.request, f"Pobrano {valid} pozycji do bazy danych.")

        return reverse_lazy('book-list')
