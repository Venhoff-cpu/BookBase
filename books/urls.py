from django.urls import path

from .views import (BookAddView, BookApiListView, BookEditView,
                    BookGoogleImportView, BookListView, LandingPage)

urlpatterns = [
    path("", LandingPage.as_view(), name="index"),
    path("book-list/", BookListView.as_view(), name="book-list"),
    path("add-book/form", BookAddView.as_view(), name="book-add"),
    path(
        "add-book/google-form",
        BookGoogleImportView.as_view(),
        name="book-add-google",
    ),
    path("book/<int:pk>", BookEditView.as_view(), name="book-edit"),
    path("api/book-list/", BookApiListView.as_view(), name="book-api"),
]
