from django.shortcuts import render
from .models import Book
from django.db.models import Q
from .forms import SearchForm


def book_list(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']

        # Secure ORM search (prevents SQL injection)
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})
