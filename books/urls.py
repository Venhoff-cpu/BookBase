from django.urls import path

from .views import BookListView, BookAddView, BookEditView, BookGoogleImportView, LandingPage

urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
    path('book-list/', BookListView.as_view(), name='book-list'),
    path('add-book/', BookAddView.as_view(), name='book-add'),
    path('book/<int:pk>', BookEditView.as_view(), name='book-edit'),
    path('google-api/', BookGoogleImportView.as_view(), name='google-api')
]

