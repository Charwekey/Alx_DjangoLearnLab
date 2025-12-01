"""
API Views for the Book model using Django REST Framework Generic Views.

This module demonstrates the use of DRF's generic views to handle CRUD operations
efficiently. Each view is configured with appropriate permissions and customizations
to meet specific API requirements.

Generic Views Used:
    - ListAPIView: Read-only endpoint for listing all books
    - RetrieveAPIView: Read-only endpoint for retrieving a single book
    - CreateAPIView: Endpoint for creating new books
    - UpdateAPIView: Endpoint for updating existing books
    - DestroyAPIView: Endpoint for deleting books

Permissions:
    - Read operations (List, Retrieve): Open to all users (authenticated or not)
    - Write operations (Create, Update, Delete): Restricted to authenticated users only
"""

from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListCreateAPIView):
    """
    API view to retrieve list of books or create a new book.
    
    GET /api/books/
    - Returns list of all books
    - Supports filtering, searching, ordering
    - Permission: AllowAny (read-only)
    
    POST /api/books/
    - Creates a new book
    - Permission: IsAuthenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Permission logic: AllowAny for GET, IsAuthenticated for POST
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year']
    ordering = ['-publication_year']


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a book.
    
    GET /api/books/<id>/
    - Retrieve book details
    - Permission: AllowAny (read-only)
    
    PUT/PATCH /api/books/<id>/
    - Update book details
    - Permission: IsAuthenticated
    
    DELETE /api/books/<id>/
    - Delete book
    - Permission: IsAuthenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Permission logic: AllowAny for GET, IsAuthenticated for PUT/PATCH/DELETE
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
