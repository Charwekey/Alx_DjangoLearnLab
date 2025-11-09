from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = author.books.all()
    return books


# Query 2: All books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books


# Query 3: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = library.librarian
    return librarian


# --- Optional: For testing in Django shell ---
if __name__ == "__main__":
    # Example calls (run using `python manage.py shell < relationship_app/query_samples.py`)
    print("Books by 'J.K. Rowling':", get_books_by_author("J.K. Rowling"))
    print("Books in 'Central Library':", get_books_in_library("Central Library"))
    print("Librarian for 'Central Library':", get_librarian_for_library("Central Library"))
