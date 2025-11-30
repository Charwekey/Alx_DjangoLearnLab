"""
URL Configuration for the API app.

This module defines all URL patterns for the Book API endpoints.
Each endpoint is mapped to its corresponding generic view with
appropriate URL patterns for CRUD operations.

URL Patterns:
    - /books/ - List all books (GET)
    - /books/<int:pk>/ - Retrieve single book (GET)
    - /books/create/ - Create new book (POST)
    - /books/<int:pk>/update/ - Update book (PUT/PATCH)
    - /books/<int:pk>/delete/ - Delete book (DELETE)

Permissions:
    - List and Detail views: Open to all users
    - Create, Update, Delete views: Authenticated users only
"""

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

# App namespace for URL reversing
app_name = 'api'

urlpatterns = [
    # List all books
    # GET /api/books/
    # Returns: List of all books with optional filtering, searching, and ordering
    # Permissions: AllowAny (no authentication required)
    # Query params: ?author=1, ?publication_year=1997, ?search=Harry, ?ordering=-publication_year
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID
    # GET /api/books/<id>/
    # Returns: Single book details
    # Permissions: AllowAny (no authentication required)
    # Example: /api/books/1/
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book
    # POST /api/books/create/
    # Request body: {"title": "...", "publication_year": ..., "author": ...}
    # Returns: Created book with HTTP 201 status
    # Permissions: IsAuthenticated (must be logged in)
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book
    # PUT /api/books/<id>/update/ - Full update (all fields required)
    # PATCH /api/books/<id>/update/ - Partial update (only changed fields)
    # Request body: {"title": "...", "publication_year": ..., "author": ...}
    # Returns: Updated book with HTTP 200 status
    # Permissions: IsAuthenticated (must be logged in)
    # Example: /api/books/1/update/
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book
    # DELETE /api/books/<id>/delete/
    # Returns: HTTP 204 No Content on success
    # Permissions: IsAuthenticated (must be logged in)
    # Example: /api/books/1/delete/
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
