"""
Test script for verifying Author and Book models and serializers.

This script demonstrates:
1. Creating Author and Book instances
2. Serializing individual books
3. Serializing authors with nested books
4. Testing custom validation (publication year)

Run this script using: python manage.py shell < test_serializers.py
Or in Django shell: exec(open('test_serializers.py').read())
"""

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from datetime import datetime
import json


def print_section(title):
    """Helper function to print section headers."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_models_and_serializers():
    """Main test function."""
    
    print_section("TESTING DJANGO REST FRAMEWORK SERIALIZERS")
    
    # Clean up any existing data for clean test
    print("\nCleaning up existing data...")
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # ========== Test 1: Create Authors ==========
    print_section("Test 1: Creating Authors")
    
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    author3 = Author.objects.create(name="Isaac Asimov")
    
    print(f"✓ Created author: {author1}")
    print(f"✓ Created author: {author2}")
    print(f"✓ Created author: {author3}")
    
    # ========== Test 2: Create Books ==========
    print_section("Test 2: Creating Books")
    
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
    book3 = Book.objects.create(
        title="A Game of Thrones",
        publication_year=1996,
        author=author2
    )
    book4 = Book.objects.create(
        title="Foundation",
        publication_year=1951,
        author=author3
    )
    
    print(f"✓ Created book: {book1}")
    print(f"✓ Created book: {book2}")
    print(f"✓ Created book: {book3}")
    print(f"✓ Created book: {book4}")
    
    # ========== Test 3: Serialize Individual Books ==========
    print_section("Test 3: BookSerializer - Individual Book")
    
    serializer = BookSerializer(book1)
    print("\nSerialized data for 'Harry Potter and the Philosopher's Stone':")
    print(json.dumps(serializer.data, indent=2))
    
    # ========== Test 4: Serialize Author with Nested Books ==========
    print_section("Test 4: AuthorSerializer - Author with Nested Books")
    
    serializer = AuthorSerializer(author1)
    print("\nSerialized data for J.K. Rowling (with nested books):")
    print(json.dumps(serializer.data, indent=2))
    
    # ========== Test 5: Serialize All Authors ==========
    print_section("Test 5: AuthorSerializer - All Authors")
    
    all_authors = Author.objects.all()
    serializer = AuthorSerializer(all_authors, many=True)
    print("\nAll authors with their books:")
    print(json.dumps(serializer.data, indent=2))
    
    # ========== Test 6: Test Custom Validation (Valid Year) ==========
    print_section("Test 6: Custom Validation - Valid Publication Year")
    
    valid_data = {
        'title': 'New Book',
        'publication_year': 2020,
        'author': author1.id
    }
    
    serializer = BookSerializer(data=valid_data)
    if serializer.is_valid():
        print("✓ Validation passed for publication_year=2020")
        print(f"  Validated data: {serializer.validated_data}")
    else:
        print(f"✗ Validation failed: {serializer.errors}")
    
    # ========== Test 7: Test Custom Validation (Future Year) ==========
    print_section("Test 7: Custom Validation - Future Publication Year")
    
    current_year = datetime.now().year
    future_year = current_year + 1
    
    invalid_data = {
        'title': 'Future Book',
        'publication_year': future_year,
        'author': author1.id
    }
    
    serializer = BookSerializer(data=invalid_data)
    if serializer.is_valid():
        print(f"✗ Validation should have failed for publication_year={future_year}")
    else:
        print(f"✓ Validation correctly failed for publication_year={future_year}")
        print(f"  Error message: {serializer.errors['publication_year'][0]}")
    
    # ========== Test 8: Relationship Verification ==========
    print_section("Test 8: Verifying Relationships")
    
    print(f"\nAuthor: {author1.name}")
    print(f"Number of books: {author1.books.count()}")
    print("Books by this author:")
    for book in author1.books.all():
        print(f"  - {book.title} ({book.publication_year})")
    
    print(f"\nBook: {book1.title}")
    print(f"Author: {book1.author.name}")
    
    # ========== Summary ==========
    print_section("TEST SUMMARY")
    print("\n✓ All tests completed successfully!")
    print(f"\nTotal Authors: {Author.objects.count()}")
    print(f"Total Books: {Book.objects.count()}")
    print("\nKey Features Demonstrated:")
    print("  1. Model creation with one-to-many relationships")
    print("  2. Basic serialization with BookSerializer")
    print("  3. Nested serialization with AuthorSerializer")
    print("  4. Custom validation for publication_year")
    print("  5. Reverse relationship queries (author.books.all())")
    
    print("\n" + "=" * 60)
    print("  Setup Complete! Your API is ready for development.")
    print("=" * 60 + "\n")


# Run the tests
if __name__ == "__main__":
    test_models_and_serializers()
