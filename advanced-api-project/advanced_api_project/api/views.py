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


class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view provides a read-only endpoint that returns all Book instances
    in the database. It supports filtering, searching, and ordering to help
    clients find specific books.
    
    **Endpoint:** GET /api/books/
    
    **Permissions:** 
        - AllowAny: No authentication required for reading book list
    
    **Features:**
        - Filtering: Filter books by author or publication year
        - Searching: Search books by title
        - Ordering: Sort books by any field (e.g., ?ordering=-publication_year)
    
    **Query Parameters:**
        - author: Filter by author ID (e.g., ?author=1)
        - publication_year: Filter by year (e.g., ?publication_year=1997)
        - search: Search in book titles (e.g., ?search=Harry)
        - ordering: Order results (e.g., ?ordering=-publication_year)
    
    **Example Response:**
        [
            {
                "id": 1,
                "title": "Harry Potter",
                "publication_year": 1997,
                "author": 1
            },
            ...
        ]
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view the list
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']  # Fields that can be filtered
    search_fields = ['title']  # Fields that can be searched
    ordering_fields = ['title', 'publication_year']  # Fields that can be used for ordering
    ordering = ['-publication_year']  # Default ordering (newest first)
    
    def get_queryset(self):
        """
        Optionally customize the queryset.
        
        This method can be overridden to add custom filtering logic,
        such as filtering based on the current user or other dynamic criteria.
        """
        queryset = super().get_queryset()
        # Example: You could add custom filtering here
        # queryset = queryset.filter(some_condition=True)
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by ID.
    
    This view provides a read-only endpoint that returns detailed information
    about a specific Book instance identified by its primary key.
    
    **Endpoint:** GET /api/books/<id>/
    
    **Permissions:**
        - AllowAny: No authentication required for reading book details
    
    **URL Parameters:**
        - pk (int): The primary key (ID) of the book to retrieve
    
    **Example Response:**
        {
            "id": 1,
            "title": "Harry Potter and the Philosopher's Stone",
            "publication_year": 1997,
            "author": 1
        }
    
    **Error Responses:**
        - 404 Not Found: If book with given ID doesn't exist
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view book details
    lookup_field = 'pk'  # Use primary key for lookup (default)


class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    This view provides an endpoint for creating new Book instances.
    Only authenticated users can create books. The view automatically
    handles data validation through the BookSerializer.
    
    **Endpoint:** POST /api/books/create/
    
    **Permissions:**
        - IsAuthenticated: Only authenticated users can create books
    
    **Request Body:**
        {
            "title": "Book Title",
            "publication_year": 2020,
            "author": 1
        }
    
    **Validation:**
        - title: Required, max 200 characters
        - publication_year: Required, cannot be in the future (custom validation)
        - author: Required, must be a valid author ID
    
    **Success Response (201 Created):**
        {
            "id": 5,
            "title": "Book Title",
            "publication_year": 2020,
            "author": 1
        }
    
    **Error Responses:**
        - 400 Bad Request: Invalid data (e.g., future publication year)
        - 401 Unauthorized: User not authenticated
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in to create
    
    def perform_create(self, serializer):
        """
        Customize the creation process.
        
        This method is called after validation but before saving the instance.
        You can add custom logic here, such as setting additional fields
        or performing side effects.
        
        Args:
            serializer: The validated serializer instance
        """
        # Save the book instance
        # You could add custom logic here, e.g.:
        # serializer.save(created_by=self.request.user)
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Override create to add custom response handling.
        
        This demonstrates how to customize the creation response,
        such as adding custom headers or modifying the response data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # You can customize the response here
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    This view provides endpoints for updating Book instances.
    Supports both full updates (PUT) and partial updates (PATCH).
    Only authenticated users can update books.
    
    **Endpoints:**
        - PUT /api/books/<id>/update/ - Full update (all fields required)
        - PATCH /api/books/<id>/update/ - Partial update (only changed fields)
    
    **Permissions:**
        - IsAuthenticated: Only authenticated users can update books
    
    **URL Parameters:**
        - pk (int): The primary key (ID) of the book to update
    
    **Request Body (PUT - all fields required):**
        {
            "title": "Updated Title",
            "publication_year": 2021,
            "author": 1
        }
    
    **Request Body (PATCH - only changed fields):**
        {
            "title": "Updated Title"
        }
    
    **Success Response (200 OK):**
        {
            "id": 1,
            "title": "Updated Title",
            "publication_year": 2021,
            "author": 1
        }
    
    **Error Responses:**
        - 400 Bad Request: Invalid data
        - 401 Unauthorized: User not authenticated
        - 404 Not Found: Book with given ID doesn't exist
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in to update
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """
        Customize the update process.
        
        This method is called after validation but before saving the updated instance.
        You can add custom logic here, such as tracking who made the update.
        
        Args:
            serializer: The validated serializer instance
        """
        # Save the updated book instance
        # You could add custom logic here, e.g.:
        # serializer.save(updated_by=self.request.user, updated_at=timezone.now())
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    This view provides an endpoint for deleting Book instances.
    Only authenticated users can delete books. Once deleted, the
    book cannot be recovered.
    
    **Endpoint:** DELETE /api/books/<id>/delete/
    
    **Permissions:**
        - IsAuthenticated: Only authenticated users can delete books
    
    **URL Parameters:**
        - pk (int): The primary key (ID) of the book to delete
    
    **Success Response (204 No Content):**
        No response body, just HTTP 204 status code
    
    **Error Responses:**
        - 401 Unauthorized: User not authenticated
        - 404 Not Found: Book with given ID doesn't exist
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in to delete
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        """
        Customize the deletion process.
        
        This method is called before deleting the instance.
        You can add custom logic here, such as soft deletes or logging.
        
        Args:
            instance: The Book instance to be deleted
        """
        # Perform the deletion
        # You could implement soft delete here instead:
        # instance.is_deleted = True
        # instance.save()
        instance.delete()
