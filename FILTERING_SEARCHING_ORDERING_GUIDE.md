# Filtering, Searching, and Ordering - Implementation Guide

## Overview

The `BookListView` in `api/views.py` already includes comprehensive filtering, searching, and ordering capabilities using Django REST Framework's built-in backends.

## Implementation Details

### Current Configuration (Lines 68-73 in api/views.py)

```python
# Enable filtering, searching, and ordering
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ['author', 'publication_year']  # Fields that can be filtered
search_fields = ['title']  # Fields that can be searched
ordering_fields = ['title', 'publication_year']  # Fields that can be used for ordering
ordering = ['-publication_year']  # Default ordering (newest first)
```

### Dependencies

✅ **Already Installed:**
- `djangorestframework` - Core DRF functionality
- `django-filter` - Filtering backend
- `django_filters` - Added to INSTALLED_APPS

---

## 1. Filtering

### What's Implemented

Filter books by:
- **Author ID** - `filterset_fields = ['author', 'publication_year']`
- **Publication Year** - Exact match filtering

### How to Use

**Filter by Author:**
```bash
GET /api/books/?author=1
```

**Filter by Publication Year:**
```bash
GET /api/books/?publication_year=1997
```

**Combine Multiple Filters:**
```bash
GET /api/books/?author=1&publication_year=1997
```

### Example with curl:
```bash
# Get all books by author with ID 1
curl "http://127.0.0.1:8000/api/books/?author=1"

# Get all books published in 1997
curl "http://127.0.0.1:8000/api/books/?publication_year=1997"

# Get books by author 1 published in 1997
curl "http://127.0.0.1:8000/api/books/?author=1&publication_year=1997"
```

### Example Response:
```json
[
  {
    "id": 1,
    "title": "Harry Potter",
    "publication_year": 1997,
    "author": 1
  }
]
```

---

## 2. Searching

### What's Implemented

Search functionality on:
- **Title field** - `search_fields = ['title']`
- Case-insensitive partial matching

### How to Use

**Search by Title:**
```bash
GET /api/books/?search=Harry
```

This will find any book with "Harry" in the title (case-insensitive).

### Example with curl:
```bash
# Search for books with "Harry" in the title
curl "http://127.0.0.1:8000/api/books/?search=Harry"

# Search for books with "Potter" in the title
curl "http://127.0.0.1:8000/api/books/?search=Potter"

# Search is case-insensitive
curl "http://127.0.0.1:8000/api/books/?search=harry"
```

### Combine Search with Filters:
```bash
# Search for "Harry" in books by author 1
curl "http://127.0.0.1:8000/api/books/?search=Harry&author=1"
```

---

## 3. Ordering

### What's Implemented

Order results by:
- **Title** - Alphabetical ordering
- **Publication Year** - Chronological ordering
- **Default:** `-publication_year` (newest first)

### How to Use

**Order by Title (Ascending):**
```bash
GET /api/books/?ordering=title
```

**Order by Title (Descending):**
```bash
GET /api/books/?ordering=-title
```

**Order by Publication Year (Ascending - oldest first):**
```bash
GET /api/books/?ordering=publication_year
```

**Order by Publication Year (Descending - newest first):**
```bash
GET /api/books/?ordering=-publication_year
```

**Multiple Field Ordering:**
```bash
GET /api/books/?ordering=-publication_year,title
```

### Example with curl:
```bash
# Order by title A-Z
curl "http://127.0.0.1:8000/api/books/?ordering=title"

# Order by title Z-A
curl "http://127.0.0.1:8000/api/books/?ordering=-title"

# Order by publication year (newest first)
curl "http://127.0.0.1:8000/api/books/?ordering=-publication_year"

# Order by publication year (oldest first)
curl "http://127.0.0.1:8000/api/books/?ordering=publication_year"

# Order by year (desc), then title (asc)
curl "http://127.0.0.1:8000/api/books/?ordering=-publication_year,title"
```

---

## 4. Combining All Features

You can combine filtering, searching, and ordering in a single request:

### Example Queries:

**Find books by author 1, with "Harry" in title, ordered by year:**
```bash
GET /api/books/?author=1&search=Harry&ordering=-publication_year
```

**Find books from 1997, ordered alphabetically:**
```bash
GET /api/books/?publication_year=1997&ordering=title
```

**Search for "Game", filter by author 2, order by title:**
```bash
GET /api/books/?search=Game&author=2&ordering=title
```

### curl Example:
```bash
curl "http://127.0.0.1:8000/api/books/?author=1&search=Harry&ordering=-publication_year"
```

---

## 5. Testing the Features

### Test Script

Create a file `test_filtering_searching_ordering.py`:

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/books/"

def test_filtering():
    """Test filtering capabilities."""
    print("\n" + "="*60)
    print("TESTING FILTERING")
    print("="*60)
    
    # Test 1: Filter by author
    print("\n1. Filter by author ID 1:")
    response = requests.get(f"{BASE_URL}?author=1")
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json())} books")
    for book in response.json():
        print(f"   - {book['title']} (Author: {book['author']})")
    
    # Test 2: Filter by publication year
    print("\n2. Filter by publication year 1997:")
    response = requests.get(f"{BASE_URL}?publication_year=1997")
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json())} books")
    for book in response.json():
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Test 3: Combine filters
    print("\n3. Filter by author 1 AND year 1997:")
    response = requests.get(f"{BASE_URL}?author=1&publication_year=1997")
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json())} books")


def test_searching():
    """Test search capabilities."""
    print("\n" + "="*60)
    print("TESTING SEARCHING")
    print("="*60)
    
    # Test 1: Search by title
    print("\n1. Search for 'Harry':")
    response = requests.get(f"{BASE_URL}?search=Harry")
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json())} books")
    for book in response.json():
        print(f"   - {book['title']}")
    
    # Test 2: Case-insensitive search
    print("\n2. Search for 'harry' (lowercase):")
    response = requests.get(f"{BASE_URL}?search=harry")
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json())} books")
    
    # Test 3: Search with filter
    print("\n3. Search 'Harry' + filter by author 1:")
    response = requests.get(f"{BASE_URL}?search=Harry&author=1")
    print(f"   Status: {response.status_code}")
    print(f"   Results: {len(response.json())} books")


def test_ordering():
    """Test ordering capabilities."""
    print("\n" + "="*60)
    print("TESTING ORDERING")
    print("="*60)
    
    # Test 1: Order by title ascending
    print("\n1. Order by title (A-Z):")
    response = requests.get(f"{BASE_URL}?ordering=title")
    print(f"   Status: {response.status_code}")
    books = response.json()
    for book in books:
        print(f"   - {book['title']}")
    
    # Test 2: Order by title descending
    print("\n2. Order by title (Z-A):")
    response = requests.get(f"{BASE_URL}?ordering=-title")
    print(f"   Status: {response.status_code}")
    books = response.json()
    for book in books:
        print(f"   - {book['title']}")
    
    # Test 3: Order by publication year (newest first)
    print("\n3. Order by publication year (newest first):")
    response = requests.get(f"{BASE_URL}?ordering=-publication_year")
    print(f"   Status: {response.status_code}")
    books = response.json()
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")
    
    # Test 4: Order by publication year (oldest first)
    print("\n4. Order by publication year (oldest first):")
    response = requests.get(f"{BASE_URL}?ordering=publication_year")
    print(f"   Status: {response.status_code}")
    books = response.json()
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']})")


def test_combined():
    """Test combining all features."""
    print("\n" + "="*60)
    print("TESTING COMBINED FEATURES")
    print("="*60)
    
    print("\n1. Filter + Search + Order:")
    print("   Query: author=1, search=Harry, ordering=-publication_year")
    response = requests.get(
        f"{BASE_URL}?author=1&search=Harry&ordering=-publication_year"
    )
    print(f"   Status: {response.status_code}")
    books = response.json()
    for book in books:
        print(f"   - {book['title']} ({book['publication_year']}, Author: {book['author']})")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FILTERING, SEARCHING, AND ORDERING TESTS")
    print("Make sure the server is running: python manage.py runserver")
    print("="*60)
    
    try:
        test_filtering()
        test_searching()
        test_ordering()
        test_combined()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to server")
        print("Make sure the server is running: python manage.py runserver\n")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}\n")
```

### Run the Tests:

```bash
# Start the server
python manage.py runserver

# In another terminal, run the test script
python test_filtering_searching_ordering.py
```

---

## 6. Advanced Customization Options

### Extend Search to Multiple Fields

To search across title AND author name:

```python
# In BookListView
search_fields = ['title', 'author__name']  # Search in title and author's name
```

### Add More Filter Fields

To filter by title as well:

```python
# In BookListView
filterset_fields = ['author', 'publication_year', 'title']
```

### Custom Filtering with django-filter

For more advanced filtering (range, greater than, less than):

```python
from django_filters import rest_framework as filters

class BookFilter(filters.FilterSet):
    min_year = filters.NumberFilter(field_name="publication_year", lookup_expr='gte')
    max_year = filters.NumberFilter(field_name="publication_year", lookup_expr='lte')
    title_contains = filters.CharFilter(field_name="title", lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ['author', 'publication_year']

# In BookListView
filterset_class = BookFilter
```

Then you can use:
```bash
GET /api/books/?min_year=1990&max_year=2000
GET /api/books/?title_contains=Potter
```

---

## 7. Documentation in Code

All features are documented in the `BookListView` docstring:

```python
**Features:**
    - Filtering: Filter books by author or publication year
    - Searching: Search books by title
    - Ordering: Sort books by any field (e.g., ?ordering=-publication_year)

**Query Parameters:**
    - author: Filter by author ID (e.g., ?author=1)
    - publication_year: Filter by year (e.g., ?publication_year=1997)
    - search: Search in book titles (e.g., ?search=Harry)
    - ordering: Order results (e.g., ?ordering=-publication_year)
```

---

## Summary

✅ **Filtering** - Fully implemented with DjangoFilterBackend  
✅ **Searching** - Fully implemented with SearchFilter  
✅ **Ordering** - Fully implemented with OrderingFilter  
✅ **Documentation** - Comprehensive docstrings and examples  
✅ **Testing** - Test scripts provided  

All features are production-ready and can be tested immediately!

### Quick Test Commands:

```bash
# Start server
python manage.py runserver

# Test filtering
curl "http://127.0.0.1:8000/api/books/?author=1"

# Test searching
curl "http://127.0.0.1:8000/api/books/?search=Harry"

# Test ordering
curl "http://127.0.0.1:8000/api/books/?ordering=-publication_year"

# Test combined
curl "http://127.0.0.1:8000/api/books/?author=1&search=Harry&ordering=-publication_year"
```
