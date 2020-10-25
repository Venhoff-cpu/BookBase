from django_filters import CharFilter, FilterSet, NumberFilter, DateTimeFilter

from .models import Book


class BookApiFilter(FilterSet):
    author = CharFilter(field_name="author", lookup_expr="icontains")
    title = CharFilter(field_name="title", lookup_expr="icontains")

    publication_date__gte = DateTimeFilter(
        field_name="publication_date", lookup_expr="gte"
    )
    publication_date__lte = DateTimeFilter(
        field_name="publication_date", lookup_expr="lte"
    )

    book_language = CharFilter(
        field_name="book_language", lookup_expr="icontains"
    )

    class Meta:
        model = Book
        fields = ["author", "title", "publication_date", "book_language"]
