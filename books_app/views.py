import urllib.parse

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, UpdateView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from .api_procesor import fetch_book_data, process_book_data
from .filters import BookApiFilter
from .forms import BookAddForm, BookSearchForm, GoogleBooksForm
from .models import Book
from .serializers import BookSerializer


class LandingPage(TemplateView):
    template_name = "books_app/index.html"

    def get_context_data(self, **kwargs):
        ctx = super(LandingPage, self).get_context_data(**kwargs)
        ctx["book_count"] = Book.objects.all().count() or 0
        return ctx


class BookListView(ListView):
    model = Book
    template_name = "books_app/book_list.html"
    paginate_by = 10

    def search_args(self):
        search_args = {}
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            search_args["author__icontains"] = form.cleaned_data["author"]
            search_args["title__icontains"] = form.cleaned_data["title"]
            search_args["book_language__icontains"] = form.cleaned_data[
                "language"
            ]
            search_args["publication_date__gte"] = \
                form.cleaned_data[
                "date_from"
            ]
            search_args["publication_date__lte"] = form.cleaned_data["date_to"]

        else:
            messages.error(self.request, "Proszę poprawić błąd w formularzu")

        # Sprawdzenie czy nie ma pustych wartości
        search_args = {
            key: value for key, value in search_args.items() if value
        }

        return search_args

    def get_context_data(self, **kwargs):
        ctx = super(BookListView, self).get_context_data(**kwargs)
        ctx["form"] = BookSearchForm()
        return ctx

    def get_queryset(self):
        search = self.search_args()
        query = super(BookListView, self).get_queryset().filter(**search)
        return query


class BookAddView(FormView):
    form_class = BookAddForm
    fields = "__all__"
    template_name = "books_app/book_add.html"
    success_url = reverse_lazy("book-list")

    def form_valid(self, form):
        new_book = Book.objects.create(
            author=form.cleaned_data["author"],
            title=form.cleaned_data["title"],
            isbn=form.cleaned_data["isbn"],
            publication_date=form.cleaned_data["publication_date"],
            page_num=form.cleaned_data["page_num"],
            link_to_cover=form.cleaned_data["link_to_cover"],
            book_language=form.cleaned_data["book_language"],
        )
        messages.success(self.request, f"Pomyślnie dodano książkę do bazy - {new_book} ")
        return super().form_valid(form)


class BookEditView(SuccessMessageMixin, UpdateView):
    template_name = "books_app/book_edit.html"
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("index")
    success_message = "Książka została pomyślnie zaktualizowana."


class BookGoogleImportView(FormView):
    template_name = "books_app/book_google_api.html"
    form_class = GoogleBooksForm

    def form_valid(self, form):
        key_word = form.cleaned_data["key_word"]
        in_title = form.cleaned_data["in_title"]
        in_author = form.cleaned_data["in_author"]

        if not key_word:
            messages.error(self.request, "Słowo kluczowe jest wymagane.")
            return reverse_lazy("book-add-google")

        q = urllib.parse.quote_plus(key_word)

        if in_title:
            q += f"+intitle:{urllib.parse.quote_plus(in_title)}"

        if in_author:
            q += f"+inauthor:{urllib.parse.quote_plus(in_author)}"

        response = fetch_book_data(q)
        number_of_items = response["totalItems"]
        if not number_of_items:
            messages.error(
                self.request, "Zapytanie nie zwróciło żdanych wartości"
            )
            return reverse_lazy("book-add-google")

        book_objs = process_book_data(response)
        Book.objects.bulk_create(book_objs, ignore_conflicts=True)

        messages.info(
            self.request,
            f"Znaleziono {number_of_items} pozycji do bazy danych. "
            f"(Maksymalna ilośc zaimportpowanych książek to 10)",
        )

        return redirect("book-list")


class BookApiListView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = BookApiFilter
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
