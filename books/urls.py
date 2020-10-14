from django.urls import path

from .views import BookListView, BookAddView, BookEditView, BookGoogleImportView

urlpatterns = [
    path('book-list/', BookListView.as_view(), name='index'),
    path('add-book/', BookAddView.as_view(), name='book-add'),
    path('book/<int:pk>', BookEditView.as_view(), name='book-edit'),
]

