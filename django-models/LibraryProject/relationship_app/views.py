from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})


# Class-based view to show details of a specific library
class LibraryDetailView(View):
    template_name = 'library_detail.html'

    def get(self, request, pk):
        library = get_object_or_404(Library, pk=pk)
        return render(request, self.template_name, {'library': library})
