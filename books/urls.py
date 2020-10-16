from django.urls import path, include

from rest_framework import routers

from .views import BookListView, BookAddView, BookEditView, BookGoogleImportView, LandingPage, BookApiListView


urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
    path('book-list/', BookListView.as_view(), name='book-list'),
    path('add-book/', BookAddView.as_view(), name='book-add'),
    path('book/<int:pk>', BookEditView.as_view(), name='book-edit'),
    path('api/book-list/', BookApiListView.as_view(), name='book-api'),
]

