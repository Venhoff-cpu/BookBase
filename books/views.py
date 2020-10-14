from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, View, UpdateView

from .models import Book
from .forms import BookAddForm


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 25


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


class BookGoogleImportView(View):
    pass
