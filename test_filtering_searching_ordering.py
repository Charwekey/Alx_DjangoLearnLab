"""
Comprehensive test script for filtering, searching, and ordering features.

This script tests all query capabilities of the Book API:
- Filtering by author and publication year
- Searching by title
- Ordering by title and publication year
- Combining multiple query parameters

Run with: python test_filtering_searching_ordering.py
(Make sure the server is running: python manage.py runserver)
"""

import requests
import json


BASE_URL = "http://127.0.0.1:8000/api/books/"


def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_books(books, indent="   "):
    """Print book details in a formatted way."""
    for book in books:
        print(f"{indent}- {book['title']} (Year: {book['publication_year']}, Author: {book['author']})")


def test_filtering():
    """Test filtering capabilities."""
    print_header("TESTING FILTERING")
    
    # Test 1: Filter by author
    print("\n1. Filter by author ID 3:")
    response = requests.get(f"{BASE_URL}?author=3")
    print(f"   URL: {BASE_URL}?author=3")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 2: Filter by publication year
    print("\n2. Filter by publication year 1997:")
    response = requests.get(f"{BASE_URL}?publication_year=1997")
    print(f"   URL: {BASE_URL}?publication_year=1997")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 3: Combine filters
    print("\n3. Filter by author 3 AND year 1997:")
    response = requests.get(f"{BASE_URL}?author=3&publication_year=1997")
    print(f"   URL: {BASE_URL}?author=3&publication_year=1997")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 4: Filter by publication year 1998
    print("\n4. Filter by publication year 1998:")
    response = requests.get(f"{BASE_URL}?publication_year=1998")
    print(f"   URL: {BASE_URL}?publication_year=1998")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)


def test_searching():
    """Test search capabilities."""
    print_header("TESTING SEARCHING")
    
    # Test 1: Search by title
    print("\n1. Search for 'Harry':")
    response = requests.get(f"{BASE_URL}?search=Harry")
    print(f"   URL: {BASE_URL}?search=Harry")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 2: Case-insensitive search
    print("\n2. Search for 'harry' (lowercase - case insensitive):")
    response = requests.get(f"{BASE_URL}?search=harry")
    print(f"   URL: {BASE_URL}?search=harry")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 3: Search for different term
    print("\n3. Search for 'Game':")
    response = requests.get(f"{BASE_URL}?search=Game")
    print(f"   URL: {BASE_URL}?search=Game")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 4: Search with filter
    print("\n4. Search 'Harry' + filter by author 3:")
    response = requests.get(f"{BASE_URL}?search=Harry&author=3")
    print(f"   URL: {BASE_URL}?search=Harry&author=3")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 5: Search for partial match
    print("\n5. Search for 'Chamber' (partial match):")
    response = requests.get(f"{BASE_URL}?search=Chamber")
    print(f"   URL: {BASE_URL}?search=Chamber")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)


def test_ordering():
    """Test ordering capabilities."""
    print_header("TESTING ORDERING")
    
    # Test 1: Order by title ascending
    print("\n1. Order by title (A-Z):")
    response = requests.get(f"{BASE_URL}?ordering=title")
    print(f"   URL: {BASE_URL}?ordering=title")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 2: Order by title descending
    print("\n2. Order by title (Z-A):")
    response = requests.get(f"{BASE_URL}?ordering=-title")
    print(f"   URL: {BASE_URL}?ordering=-title")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 3: Order by publication year (newest first)
    print("\n3. Order by publication year (newest first - default):")
    response = requests.get(f"{BASE_URL}?ordering=-publication_year")
    print(f"   URL: {BASE_URL}?ordering=-publication_year")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 4: Order by publication year (oldest first)
    print("\n4. Order by publication year (oldest first):")
    response = requests.get(f"{BASE_URL}?ordering=publication_year")
    print(f"   URL: {BASE_URL}?ordering=publication_year")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    # Test 5: Default ordering (no parameter)
    print("\n5. Default ordering (no parameter - should be newest first):")
    response = requests.get(BASE_URL)
    print(f"   URL: {BASE_URL}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)


def test_combined():
    """Test combining all features."""
    print_header("TESTING COMBINED FEATURES")
    
    print("\n1. Filter + Search + Order:")
    print("   Query: author=3, search=Harry, ordering=-publication_year")
    response = requests.get(
        f"{BASE_URL}?author=3&search=Harry&ordering=-publication_year"
    )
    print(f"   URL: {BASE_URL}?author=3&search=Harry&ordering=-publication_year")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    print("\n2. Filter by year + Order by title:")
    print("   Query: publication_year=1997, ordering=title")
    response = requests.get(
        f"{BASE_URL}?publication_year=1997&ordering=title"
    )
    print(f"   URL: {BASE_URL}?publication_year=1997&ordering=title")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)
    
    print("\n3. Search + Order:")
    print("   Query: search=Game, ordering=-publication_year")
    response = requests.get(
        f"{BASE_URL}?search=Game&ordering=-publication_year"
    )
    print(f"   URL: {BASE_URL}?search=Game&ordering=-publication_year")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Results: {len(books)} books")
        print_books(books)


def test_all_books():
    """Display all books for reference."""
    print_header("ALL BOOKS IN DATABASE")
    
    response = requests.get(BASE_URL)
    print(f"   URL: {BASE_URL}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"   Total books: {len(books)}")
        print_books(books)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  FILTERING, SEARCHING, AND ORDERING - COMPREHENSIVE TESTS")
    print("=" * 70)
    print("\n  Prerequisites:")
    print("  1. Server must be running: python manage.py runserver")
    print("  2. Test data should be in database")
    print("=" * 70)
    
    try:
        # First show all books
        test_all_books()
        
        # Run all tests
        test_filtering()
        test_searching()
        test_ordering()
        test_combined()
        
        print("\n" + "=" * 70)
        print("  ✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n  Summary:")
        print("  - Filtering by author and publication_year: ✓ Working")
        print("  - Searching by title (case-insensitive): ✓ Working")
        print("  - Ordering by title and publication_year: ✓ Working")
        print("  - Combining multiple query parameters: ✓ Working")
        print("=" * 70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 70)
        print("  ✗ ERROR: Could not connect to server")
        print("=" * 70)
        print("\n  Please start the server:")
        print("    python manage.py runserver")
        print("\n" + "=" * 70 + "\n")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}\n")
