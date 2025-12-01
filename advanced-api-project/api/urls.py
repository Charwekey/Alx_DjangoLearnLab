"""
URL Configuration for the API app.

This module defines all URL patterns for the Book API endpoints.
Each endpoint is mapped to its corresponding generic view with
appropriate URL patterns for CRUD operations.

URL Patterns:
    - /books/ - List all books (GET) and Create new book (POST)
    - /books/<int:pk>/ - Retrieve (GET), Update (PUT/PATCH), and Delete (DELETE) book

Permissions:
    - List and Detail views: Open to all users (read-only)
    - Create, Update, Delete views: Authenticated users only
"""

from django.urls import path
from .views import (
    BookListView,
    BookDetailView
)

# App namespace for URL reversing
app_name = 'api'

urlpatterns = [
    # List and Create books
    # GET /api/books/ - List all books
    # POST /api/books/ - Create new book
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve, Update, and Delete book
    # GET /api/books/<id>/ - Retrieve
    # PUT/PATCH /api/books/<id>/ - Update
    # DELETE /api/books/<id>/ - Delete
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
