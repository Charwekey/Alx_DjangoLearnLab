# Django REST Framework - Quick Reference Guide

## Testing Your Serializers

### Using Django Shell

Start the Django shell:
```bash
python manage.py shell
```

### Create Test Data

```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George R.R. Martin")

# Create books
book1 = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    publication_year=1997,
    author=author1
)
book2 = Book.objects.create(
    title="Harry Potter and the Chamber of Secrets",
    publication_year=1998,
    author=author1
)
```

### Test BookSerializer

```python
# Serialize a single book
serializer = BookSerializer(book1)
print(serializer.data)
# Output: {'id': 1, 'title': 'Harry Potter...', 'publication_year': 1997, 'author': 1}

# Serialize multiple books
books = Book.objects.all()
serializer = BookSerializer(books, many=True)
print(serializer.data)
```

### Test AuthorSerializer with Nested Books

```python
# Serialize author with all their books
serializer = AuthorSerializer(author1)
print(serializer.data)
# Output includes nested books array

# Serialize all authors with their books
authors = Author.objects.all()
serializer = AuthorSerializer(authors, many=True)
print(serializer.data)
```

### Test Custom Validation

```python
from datetime import datetime

# Valid data
valid_data = {
    'title': 'New Book',
    'publication_year': 2020,
    'author': author1.id
}
serializer = BookSerializer(data=valid_data)
print(serializer.is_valid())  # True

# Invalid data (future year)
future_year = datetime.now().year + 1
invalid_data = {
    'title': 'Future Book',
    'publication_year': future_year,
    'author': author1.id
}
serializer = BookSerializer(data=invalid_data)
print(serializer.is_valid())  # False
print(serializer.errors)  # Shows validation error
```

## Using Django Admin

### Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### Access Admin Panel

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to: http://127.0.0.1:8000/admin/

3. Log in with your superuser credentials

4. You can now:
   - Add/edit/delete Authors
   - Add/edit/delete Books
   - See the relationship between authors and books

## Model Relationships

### Access Books from Author

```python
author = Author.objects.get(name="J.K. Rowling")
books = author.books.all()  # Get all books by this author
print(f"{author.name} has {books.count()} books")
```

### Access Author from Book

```python
book = Book.objects.get(title="Harry Potter...")
print(f"{book.title} was written by {book.author.name}")
```

## Key Files

- **Models:** `api/models.py` - Author and Book models
- **Serializers:** `api/serializers.py` - Custom serializers with validation
- **Admin:** `api/admin.py` - Admin panel configuration
- **Settings:** `advanced_api_project/settings.py` - Project configuration
- **Test Script:** `test_serializers.py` - Automated tests

## Next Steps

1. **Create API Views** - Add ViewSets for CRUD operations
2. **Configure URLs** - Set up API endpoints
3. **Add Authentication** - Implement user authentication
4. **Write Tests** - Create unit tests for your API
5. **Build Frontend** - Create a client to consume your API
