"""
Comprehensive Unit Tests for Django REST Framework API Views.

This module contains comprehensive unit tests for all Book API endpoints,
covering CRUD operations, filtering, searching, ordering, authentication,
permissions, and validation.

Test Classes:
    - BookListViewTests: Tests for GET /api/books/ endpoint
    - BookDetailViewTests: Tests for GET /api/books/<id>/ endpoint
    - BookCreateViewTests: Tests for POST /api/books/create/ endpoint
    - BookUpdateViewTests: Tests for PUT/PATCH /api/books/<id>/update/ endpoint
    - BookDeleteViewTests: Tests for DELETE /api/books/<id>/delete/ endpoint
    - BookFilteringTests: Tests for filtering functionality
    - BookSearchingTests: Tests for searching functionality
    - BookOrderingTests: Tests for ordering functionality
    - BookPermissionTests: Tests for authentication and permissions
    - BookValidationTests: Tests for custom validation and error handling

Usage:
    # Run all tests in this module
    python manage.py test api.test_views
    
    # Run specific test class
    python manage.py test api.test_views.BookCreateViewTests
    
    # Run specific test method
    python manage.py test api.test_views.BookCreateViewTests.test_create_book_authenticated
    
    # Run with verbose output
    python manage.py test api.test_views --verbosity=2
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime

from .models import Author, Book


class BookAPITestCase(TestCase):
    """
    Base test case class with common setup and helper methods.
    
    This class provides:
    - setUp() method to create test data
    - Helper methods for creating users, authors, and books
    - Common test fixtures used across multiple test classes
    """
    
    def setUp(self):
        """
        Set up test data before each test method.
        
        Creates:
        - API client for making requests
        - Test user for authentication
        - Test authors
        - Test books
        """
        # Create API client
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author3
        )
        self.book5 = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author3
        )
    
    def authenticate(self):
        """Authenticate the test client with the test user."""
        self.client.force_authenticate(user=self.user)
    
    def unauthenticate(self):
        """Remove authentication from the test client."""
        self.client.force_authenticate(user=None)
    
    def create_book(self, title, publication_year, author):
        """
        Helper method to create a book.
        
        Args:
            title (str): Book title
            publication_year (int): Year of publication
            author (Author): Author instance
            
        Returns:
            Book: Created book instance
        """
        return Book.objects.create(
            title=title,
            publication_year=publication_year,
            author=author
        )
    
    def create_author(self, name):
        """
        Helper method to create an author.
        
        Args:
            name (str): Author name
            
        Returns:
            Author: Created author instance
        """
        return Author.objects.create(name=name)


class BookListViewTests(BookAPITestCase):
    """
    Tests for the Book List endpoint (GET /api/books/).
    
    This endpoint should:
    - Return a list of all books
    - Be accessible without authentication
    - Support filtering, searching, and ordering
    """
    
    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)  # We created 5 books in setUp
    
    def test_list_books_authenticated(self):
        """Test that authenticated users can list books."""
        self.authenticate()
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
    
    def test_list_books_returns_correct_data(self):
        """Test that the list endpoint returns correct book data."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that response contains expected fields
        first_book = response.data[0]
        self.assertIn('id', first_book)
        self.assertIn('title', first_book)
        self.assertIn('publication_year', first_book)
        self.assertIn('author', first_book)
    
    def test_list_books_empty_database(self):
        """Test listing books when database is empty."""
        # Delete all books
        Book.objects.all().delete()
        
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class BookDetailViewTests(BookAPITestCase):
    """
    Tests for the Book Detail endpoint (GET /api/books/<id>/).
    
    This endpoint should:
    - Return details of a specific book
    - Be accessible without authentication
    - Return 404 for non-existent books
    """
    
    def test_retrieve_book_unauthenticated(self):
        """Test that unauthenticated users can retrieve book details."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.book1.author.pk)
    
    def test_retrieve_book_authenticated(self):
        """Test that authenticated users can retrieve book details."""
        self.authenticate()
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist returns 404."""
        url = reverse('api:book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_book_returns_all_fields(self):
        """Test that the detail endpoint returns all expected fields."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('title', response.data)
        self.assertIn('publication_year', response.data)
        self.assertIn('author', response.data)


class BookCreateViewTests(BookAPITestCase):
    """
    Tests for the Book Create endpoint (POST /api/books/create/).
    
    This endpoint should:
    - Allow authenticated users to create books
    - Deny unauthenticated users (401/403)
    - Validate data before creating
    """
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 6)  # 5 from setUp + 1 new
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(response.data['publication_year'], 2020)
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        url = reverse('api:book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 5)  # No new book created
    
    def test_create_book_missing_title(self):
        """Test creating a book without a title fails."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_book_missing_publication_year(self):
        """Test creating a book without publication year fails."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_missing_author(self):
        """Test creating a book without an author fails."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2020
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('author', response.data)
    
    def test_create_book_invalid_author(self):
        """Test creating a book with non-existent author fails."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': 99999  # Non-existent author ID
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('author', response.data)
    
    def test_create_book_current_year(self):
        """Test creating a book with current year is allowed."""
        self.authenticate()
        url = reverse('api:book-create')
        current_year = datetime.now().year
        data = {
            'title': 'Current Year Book',
            'publication_year': current_year,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['publication_year'], current_year)


class BookUpdateViewTests(BookAPITestCase):
    """
    Tests for the Book Update endpoint (PUT/PATCH /api/books/<id>/update/).
    
    This endpoint should:
    - Allow authenticated users to update books
    - Deny unauthenticated users (401/403)
    - Support both full (PUT) and partial (PATCH) updates
    """
    
    def test_update_book_authenticated_put(self):
        """Test that authenticated users can fully update books with PUT."""
        self.authenticate()
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Title',
            'publication_year': 1999,
            'author': self.author2.pk
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        self.assertEqual(self.book1.publication_year, 1999)
        self.assertEqual(self.book1.author.pk, self.author2.pk)
    
    def test_update_book_authenticated_patch(self):
        """Test that authenticated users can partially update books with PATCH."""
        self.authenticate()
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Partially Updated Title'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        # Other fields should remain unchanged
        self.assertEqual(self.book1.publication_year, 1997)
        self.assertEqual(self.book1.author.pk, self.author1.pk)
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Unauthorized Update'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.book1.refresh_from_db()
        # Book should not be updated
        self.assertNotEqual(self.book1.title, 'Unauthorized Update')
    
    def test_update_nonexistent_book(self):
        """Test updating a non-existent book returns 404."""
        self.authenticate()
        url = reverse('api:book-update', kwargs={'pk': 99999})
        data = {
            'title': 'Updated Title'
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_book_multiple_fields(self):
        """Test updating multiple fields at once."""
        self.authenticate()
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'New Title',
            'publication_year': 2000
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'New Title')
        self.assertEqual(self.book1.publication_year, 2000)


class BookDeleteViewTests(BookAPITestCase):
    """
    Tests for the Book Delete endpoint (DELETE /api/books/<id>/delete/).
    
    This endpoint should:
    - Allow authenticated users to delete books
    - Deny unauthenticated users (401/403)
    - Return 204 No Content on success
    """
    
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books."""
        self.authenticate()
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 4)  # 5 - 1 = 4
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 5)  # No book deleted
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_nonexistent_book(self):
        """Test deleting a non-existent book returns 404."""
        self.authenticate()
        url = reverse('api:book-delete', kwargs={'pk': 99999})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_book_twice(self):
        """Test that deleting the same book twice returns 404 on second attempt."""
        self.authenticate()
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        
        # First deletion should succeed
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)
        
        # Second deletion should fail with 404
        response2 = self.client.delete(url)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)


class BookFilteringTests(BookAPITestCase):
    """
    Tests for filtering functionality on the Book List endpoint.
    
    The endpoint should support filtering by:
    - author (author ID)
    - publication_year
    """
    
    def test_filter_by_author(self):
        """Test filtering books by author ID."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author1.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # author1 has 2 books
        for book in response.data:
            self.assertEqual(book['author'], self.author1.pk)
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only book1 published in 1997
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_filter_by_multiple_criteria(self):
        """Test filtering by multiple criteria simultaneously."""
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': self.author1.pk,
            'publication_year': 1997
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.pk)
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_filter_no_results(self):
        """Test filtering with criteria that match no books."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 2050})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_filter_by_nonexistent_author(self):
        """Test filtering by non-existent author returns 400 Bad Request (validation error)."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': 99999})
        
        # django-filter validates that the choice exists, so it returns 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookSearchingTests(BookAPITestCase):
    """
    Tests for searching functionality on the Book List endpoint.
    
    The endpoint should support searching by:
    - title (case-insensitive partial match)
    """
    
    def test_search_by_title(self):
        """Test searching books by title."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 Harry Potter books
        for book in response.data:
            self.assertIn('Harry', book['title'])
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_partial_match(self):
        """Test that search supports partial matches."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Lord'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Lord', response.data[0]['title'])
    
    def test_search_no_results(self):
        """Test searching with term that matches no books."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'NonexistentBook'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_search_empty_string(self):
        """Test searching with empty string returns all books."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': ''})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)


class BookOrderingTests(BookAPITestCase):
    """
    Tests for ordering functionality on the Book List endpoint.
    
    The endpoint should support ordering by:
    - title
    - publication_year
    - Default ordering: -publication_year (newest first)
    """
    
    def test_default_ordering(self):
        """Test that books are ordered by publication year (newest first) by default."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        # Check that years are in descending order
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_order_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_by_title_descending(self):
        """Test ordering books by title in descending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_by_publication_year_ascending(self):
        """Test ordering books by publication year in ascending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))


class BookPermissionTests(BookAPITestCase):
    """
    Tests for authentication and permission enforcement.
    
    Permission rules:
    - List and Detail views: AllowAny (no authentication required)
    - Create, Update, Delete views: IsAuthenticated (must be logged in)
    """
    
    def test_list_view_allows_unauthenticated(self):
        """Test that list view is accessible without authentication."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_view_allows_unauthenticated(self):
        """Test that detail view is accessible without authentication."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_view_requires_authentication(self):
        """Test that create view requires authentication."""
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_update_view_requires_authentication(self):
        """Test that update view requires authentication."""
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Updated Title'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_delete_view_requires_authentication(self):
        """Test that delete view requires authentication."""
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_authenticated_user_can_create(self):
        """Test that authenticated users can create books."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'Authenticated Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_authenticated_user_can_update(self):
        """Test that authenticated users can update books."""
        self.authenticate()
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Updated by Auth User'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_user_can_delete(self):
        """Test that authenticated users can delete books."""
        self.authenticate()
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BookValidationTests(BookAPITestCase):
    """
    Tests for custom validation and error handling.
    
    Validation rules:
    - publication_year cannot be in the future
    - All required fields must be provided
    - Author must exist
    """
    
    def test_future_publication_year_rejected(self):
        """Test that books with future publication years are rejected."""
        self.authenticate()
        url = reverse('api:book-create')
        future_year = datetime.now().year + 10
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_current_year_accepted(self):
        """Test that books with current year are accepted."""
        self.authenticate()
        url = reverse('api:book-create')
        current_year = datetime.now().year
        data = {
            'title': 'Current Year Book',
            'publication_year': current_year,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_past_year_accepted(self):
        """Test that books with past years are accepted."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'Old Book',
            'publication_year': 1900,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_invalid_data_type_for_year(self):
        """Test that invalid data type for publication year is rejected."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 'not-a-number',
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_empty_title_rejected(self):
        """Test that empty title is rejected."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': '',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_title_too_long_rejected(self):
        """Test that title exceeding max length is rejected."""
        self.authenticate()
        url = reverse('api:book-create')
        data = {
            'title': 'x' * 201,  # Max length is 200
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_update_with_future_year_rejected(self):
        """Test that updating a book with future year is rejected."""
        self.authenticate()
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        future_year = datetime.now().year + 10
        data = {
            'publication_year': future_year
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
