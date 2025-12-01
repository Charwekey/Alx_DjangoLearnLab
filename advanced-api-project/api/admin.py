from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.
    
    Provides a clean interface for managing authors in the Django admin panel.
    """
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    
    Provides a comprehensive interface for managing books in the Django admin panel,
    including filtering and search capabilities.
    """
    list_display = ['id', 'title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year', 'title']
    raw_id_fields = ['author']  # Use a search widget for author selection
