# Book API Documentation

## Overview

This API provides endpoints for managing books and authors using Django REST Framework. The API supports full CRUD (Create, Read, Update, Delete) operations with permission-based access control.

## Base URL

```
http://127.0.0.1:8000/api/
```

## Authentication

The API uses Django's session authentication. Write operations (Create, Update, Delete) require authentication, while read operations (List, Retrieve) are publicly accessible.

### Login

To authenticate, log in through the Django admin panel:
```
http://127.0.0.1:8000/admin/
```

**Test Credentials:**
- Username: `admin`
- Password: `admin123`

---

## Endpoints

### 1. List All Books

**Endpoint:** `GET /api/books/`

**Description:** Retrieve a list of all books with support for filtering, searching, and ordering.

**Authentication:** Not required

**Query Parameters:**
- `author` (int): Filter by author ID
- `publication_year` (int): Filter by publication year
- `search` (string): Search in book titles
- `ordering` (string): Order results by field (prefix with `-` for descending)

**Example Requests:**
```bash
# Get all books
curl http://127.0.0.1:8000/api/books/

# Filter by author
curl http://127.0.0.1:8000/api/books/?author=1

# Filter by publication year
curl http://127.0.0.1:8000/api/books/?publication_year=1997

# Search by title
curl http://127.0.0.1:8000/api/books/?search=Harry

# Order by publication year (newest first)
curl http://127.0.0.1:8000/api/books/?ordering=-publication_year

# Combine filters
curl http://127.0.0.1:8000/api/books/?author=1&ordering=-publication_year
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Harry Potter and the Philosopher's Stone",
    "publication_year": 1997,
    "author": 1
  },
  {
    "id": 2,
    "title": "Chamber of Secrets",
    "publication_year": 1998,
    "author": 1
  }
]
```

---

### 2. Retrieve Single Book

**Endpoint:** `GET /api/books/<id>/`

**Description:** Retrieve detailed information about a specific book.

**Authentication:** Not required

**URL Parameters:**
- `id` (int): The book's ID

**Example Request:**
```bash
curl http://127.0.0.1:8000/api/books/1/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Harry Potter and the Philosopher's Stone",
  "publication_year": 1997,
  "author": 1
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 3. Create New Book

**Endpoint:** `POST /api/books/create/`

**Description:** Create a new book. Requires authentication.

**Authentication:** Required (authenticated users only)

**Request Body:**
```json
{
  "title": "New Book Title",
  "publication_year": 2020,
  "author": 1
}
```

**Field Validation:**
- `title`: Required, max 200 characters
- `publication_year`: Required, cannot be in the future
- `author`: Required, must be a valid author ID

**Example Request:**
```bash
# Using curl with session authentication
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "New Book",
    "publication_year": 2020,
    "author": 1
  }'
```

**Success Response (201 Created):**
```json
{
  "id": 5,
  "title": "New Book",
  "publication_year": 2020,
  "author": 1
}
```

**Error Response (400 Bad Request):**
```json
{
  "publication_year": [
    "Publication year cannot be in the future. Current year is 2025, but got 2030."
  ]
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 4. Update Book

**Endpoint:** `PUT /api/books/<id>/update/` or `PATCH /api/books/<id>/update/`

**Description:** Update an existing book. Supports full update (PUT) or partial update (PATCH). Requires authentication.

**Authentication:** Required (authenticated users only)

**URL Parameters:**
- `id` (int): The book's ID

**Request Body (PUT - all fields required):**
```json
{
  "title": "Updated Title",
  "publication_year": 2021,
  "author": 1
}
```

**Request Body (PATCH - only changed fields):**
```json
{
  "title": "Updated Title"
}
```

**Example Requests:**
```bash
# Full update (PUT)
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Updated Book",
    "publication_year": 2021,
    "author": 1
  }'

# Partial update (PATCH)
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Updated Title Only"
  }'
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Book",
  "publication_year": 2021,
  "author": 1
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Book doesn't exist

---

### 5. Delete Book

**Endpoint:** `DELETE /api/books/<id>/delete/`

**Description:** Delete a book. Requires authentication.

**Authentication:** Required (authenticated users only)

**URL Parameters:**
- `id` (int): The book's ID

**Example Request:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -b cookies.txt
```

**Success Response (204 No Content):**
No response body, just HTTP 204 status code.

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Book doesn't exist

---

## Permission Summary

| Endpoint | Method | Authentication Required |
|----------|--------|------------------------|
| `/api/books/` | GET | No |
| `/api/books/<id>/` | GET | No |
| `/api/books/create/` | POST | Yes |
| `/api/books/<id>/update/` | PUT/PATCH | Yes |
| `/api/books/<id>/delete/` | DELETE | Yes |

---

## Custom Features

### 1. Filtering

Filter books by author or publication year:
```bash
# Books by specific author
GET /api/books/?author=1

# Books from specific year
GET /api/books/?publication_year=1997
```

### 2. Searching

Search books by title (case-insensitive):
```bash
GET /api/books/?search=harry
```

### 3. Ordering

Order results by any field:
```bash
# Ascending order
GET /api/books/?ordering=title

# Descending order
GET /api/books/?ordering=-publication_year

# Multiple fields
GET /api/books/?ordering=-publication_year,title
```

### 4. Custom Validation

The API includes custom validation to ensure data integrity:

**Publication Year Validation:**
- Books cannot have a publication year in the future
- Validation error provides current year and attempted value

Example error:
```json
{
  "publication_year": [
    "Publication year cannot be in the future. Current year is 2025, but got 2030."
  ]
}
```

---

## Testing the API

### Using curl

1. **List all books:**
   ```bash
   curl http://127.0.0.1:8000/api/books/
   ```

2. **Get a specific book:**
   ```bash
   curl http://127.0.0.1:8000/api/books/1/
   ```

3. **Create a book (requires authentication):**
   ```bash
   # First login and save cookies
   curl -c cookies.txt -d "username=admin&password=admin123" \
     http://127.0.0.1:8000/admin/login/
   
   # Then create book
   curl -X POST http://127.0.0.1:8000/api/books/create/ \
     -H "Content-Type: application/json" \
     -b cookies.txt \
     -d '{"title": "Test Book", "publication_year": 2020, "author": 1}'
   ```

### Using Python (requests library)

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# List all books
response = requests.get(f"{BASE_URL}/books/")
print(response.json())

# Get specific book
response = requests.get(f"{BASE_URL}/books/1/")
print(response.json())

# Create book (with authentication)
session = requests.Session()
# Login through admin
session.get("http://127.0.0.1:8000/admin/")
csrftoken = session.cookies.get('csrftoken')
session.post(
    "http://127.0.0.1:8000/admin/login/",
    data={
        'username': 'admin',
        'password': 'admin123',
        'csrfmiddlewaretoken': csrftoken
    }
)

# Now create book
response = session.post(
    f"{BASE_URL}/books/create/",
    json={
        "title": "New Book",
        "publication_year": 2023,
        "author": 1
    }
)
print(response.json())
```

### Using Postman

1. **Setup:**
   - Import the API endpoints
   - Set base URL: `http://127.0.0.1:8000/api`

2. **Authentication:**
   - Go to Authorization tab
   - Select "No Auth" for GET requests
   - For POST/PUT/PATCH/DELETE, login through browser first

3. **Test Endpoints:**
   - GET `/books/` - List books
   - GET `/books/1/` - Get book
   - POST `/books/create/` - Create book
   - PATCH `/books/1/update/` - Update book
   - DELETE `/books/1/delete/` - Delete book

---

## Running the Server

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the API:**
   - API Base: http://127.0.0.1:8000/api/
   - Admin Panel: http://127.0.0.1:8000/admin/

3. **Create test data:**
   ```bash
   python manage.py shell
   ```
   ```python
   from api.models import Author, Book
   
   author = Author.objects.create(name="J.K. Rowling")
   Book.objects.create(
       title="Harry Potter",
       publication_year=1997,
       author=author
   )
   ```

---

## Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## View Customizations

### Custom Methods

Each view includes customizable methods:

**BookCreateView:**
- `perform_create()`: Called after validation, before saving
- `create()`: Override to customize response

**BookUpdateView:**
- `perform_update()`: Called after validation, before saving

**BookDeleteView:**
- `perform_destroy()`: Called before deletion

**BookListView:**
- `get_queryset()`: Customize the queryset with additional filtering

### Example Customizations

```python
# Track who created a book
def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)

# Soft delete instead of hard delete
def perform_destroy(self, instance):
    instance.is_deleted = True
    instance.save()

# Filter books by current user
def get_queryset(self):
    queryset = super().get_queryset()
    if self.request.user.is_authenticated:
        return queryset.filter(created_by=self.request.user)
    return queryset
```

---

## Additional Resources

- **Django REST Framework Documentation:** https://www.django-rest-framework.org/
- **Generic Views:** https://www.django-rest-framework.org/api-guide/generic-views/
- **Permissions:** https://www.django-rest-framework.org/api-guide/permissions/
- **Filtering:** https://www.django-rest-framework.org/api-guide/filtering/
