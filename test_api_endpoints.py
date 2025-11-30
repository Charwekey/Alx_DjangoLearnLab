"""
Test script for verifying all API endpoints.

This script tests all CRUD operations on the Book API:
1. List all books (GET /api/books/)
2. Retrieve single book (GET /api/books/<id>/)
3. Create new book (POST /api/books/create/)
4. Update book (PUT/PATCH /api/books/<id>/update/)
5. Delete book (DELETE /api/books/<id>/delete/)

It also verifies permission enforcement.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

# Test credentials
USERNAME = "admin"
PASSWORD = "admin123"


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_response(response):
    """Print formatted response details."""
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    try:
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Body: {response.text}")


def get_auth_token():
    """Get authentication token (if using token auth) or return credentials."""
    # For this test, we'll use session authentication
    return None


def test_list_books_unauthenticated():
    """Test listing books without authentication (should work)."""
    print_section("TEST 1: List Books (Unauthenticated)")
    
    response = requests.get(f"{BASE_URL}/books/")
    print_response(response)
    
    if response.status_code == 200:
        print("✓ SUCCESS: Unauthenticated users can list books")
    else:
        print("✗ FAILED: Expected status 200")
    
    return response.json() if response.status_code == 200 else []


def test_detail_book_unauthenticated(book_id):
    """Test retrieving a single book without authentication (should work)."""
    print_section(f"TEST 2: Retrieve Book {book_id} (Unauthenticated)")
    
    response = requests.get(f"{BASE_URL}/books/{book_id}/")
    print_response(response)
    
    if response.status_code == 200:
        print("✓ SUCCESS: Unauthenticated users can view book details")
    else:
        print("✗ FAILED: Expected status 200")


def test_create_book_unauthenticated():
    """Test creating a book without authentication (should fail)."""
    print_section("TEST 3: Create Book (Unauthenticated - Should Fail)")
    
    data = {
        "title": "Unauthorized Book",
        "publication_year": 2020,
        "author": 1
    }
    
    response = requests.post(f"{BASE_URL}/books/create/", json=data)
    print_response(response)
    
    if response.status_code in [401, 403]:
        print("✓ SUCCESS: Unauthenticated users cannot create books")
    else:
        print("✗ FAILED: Expected status 401 or 403")


def test_create_book_authenticated(session):
    """Test creating a book with authentication (should work)."""
    print_section("TEST 4: Create Book (Authenticated)")
    
    data = {
        "title": "Test Book via API",
        "publication_year": 2023,
        "author": 1
    }
    
    response = session.post(f"{BASE_URL}/books/create/", json=data)
    print_response(response)
    
    if response.status_code == 201:
        print("✓ SUCCESS: Authenticated users can create books")
        return response.json()['id']
    else:
        print("✗ FAILED: Expected status 201")
        return None


def test_create_book_invalid_year(session):
    """Test creating a book with future year (should fail validation)."""
    print_section("TEST 5: Create Book with Future Year (Should Fail Validation)")
    
    data = {
        "title": "Future Book",
        "publication_year": 2030,
        "author": 1
    }
    
    response = session.post(f"{BASE_URL}/books/create/", json=data)
    print_response(response)
    
    if response.status_code == 400:
        print("✓ SUCCESS: Custom validation prevents future publication years")
    else:
        print("✗ FAILED: Expected status 400")


def test_update_book_authenticated(session, book_id):
    """Test updating a book with authentication (should work)."""
    print_section(f"TEST 6: Update Book {book_id} (Authenticated)")
    
    # Partial update (PATCH)
    data = {
        "title": "Updated Book Title"
    }
    
    response = session.patch(f"{BASE_URL}/books/{book_id}/update/", json=data)
    print_response(response)
    
    if response.status_code == 200:
        print("✓ SUCCESS: Authenticated users can update books")
    else:
        print("✗ FAILED: Expected status 200")


def test_delete_book_unauthenticated(book_id):
    """Test deleting a book without authentication (should fail)."""
    print_section(f"TEST 7: Delete Book {book_id} (Unauthenticated - Should Fail)")
    
    response = requests.delete(f"{BASE_URL}/books/{book_id}/delete/")
    print_response(response)
    
    if response.status_code in [401, 403]:
        print("✓ SUCCESS: Unauthenticated users cannot delete books")
    else:
        print("✗ FAILED: Expected status 401 or 403")


def test_delete_book_authenticated(session, book_id):
    """Test deleting a book with authentication (should work)."""
    print_section(f"TEST 8: Delete Book {book_id} (Authenticated)")
    
    response = session.delete(f"{BASE_URL}/books/{book_id}/delete/")
    print_response(response)
    
    if response.status_code == 204:
        print("✓ SUCCESS: Authenticated users can delete books")
    else:
        print("✗ FAILED: Expected status 204")


def test_filtering_and_search():
    """Test filtering and search functionality."""
    print_section("TEST 9: Filtering and Search")
    
    # Test filtering by publication year
    print("\n--- Filter by publication year ---")
    response = requests.get(f"{BASE_URL}/books/?publication_year=1997")
    print(f"Filter by year 1997: {response.status_code}")
    if response.status_code == 200:
        print(f"Results: {len(response.json())} books")
    
    # Test search
    print("\n--- Search by title ---")
    response = requests.get(f"{BASE_URL}/books/?search=Harry")
    print(f"Search for 'Harry': {response.status_code}")
    if response.status_code == 200:
        print(f"Results: {len(response.json())} books")
    
    # Test ordering
    print("\n--- Ordering ---")
    response = requests.get(f"{BASE_URL}/books/?ordering=-publication_year")
    print(f"Order by publication year (desc): {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        if books:
            print(f"First book year: {books[0].get('publication_year')}")


def run_all_tests():
    """Run all API tests."""
    print_section("STARTING API ENDPOINT TESTS")
    print("Make sure the development server is running!")
    print("Run: python manage.py runserver")
    
    try:
        # Test unauthenticated read operations
        books = test_list_books_unauthenticated()
        
        if books:
            test_detail_book_unauthenticated(books[0]['id'])
        
        # Test unauthenticated write operations (should fail)
        test_create_book_unauthenticated()
        
        # Create authenticated session
        session = requests.Session()
        
        # Login (using Django session authentication)
        # First, get CSRF token
        session.get(f"http://127.0.0.1:8000/admin/")
        csrftoken = session.cookies.get('csrftoken')
        
        # Login
        login_data = {
            'username': USERNAME,
            'password': PASSWORD,
            'csrfmiddlewaretoken': csrftoken
        }
        session.post(
            "http://127.0.0.1:8000/admin/login/",
            data=login_data,
            headers={'Referer': 'http://127.0.0.1:8000/admin/'}
        )
        
        # Test authenticated operations
        new_book_id = test_create_book_authenticated(session)
        test_create_book_invalid_year(session)
        
        if new_book_id:
            test_update_book_authenticated(session, new_book_id)
            test_delete_book_unauthenticated(new_book_id)
            test_delete_book_authenticated(session, new_book_id)
        
        # Test filtering and search
        test_filtering_and_search()
        
        print_section("ALL TESTS COMPLETED")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to the server.")
        print("Make sure the development server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
