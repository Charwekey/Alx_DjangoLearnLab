"""
Custom serializers for the API app.

This module contains serializers for the Author and Book models, demonstrating
advanced Django REST Framework features including nested serialization and
custom validation.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book instances,
    including all fields from the Book model. It implements custom validation to
    ensure data integrity.
    
    Fields:
        - id: Auto-generated primary key (read-only)
        - title: The title of the book
        - publication_year: The year the book was published
        - author: Foreign key reference to the Author model
    
    Custom Validation:
        - validate_publication_year: Ensures the publication year is not in the future.
          This prevents users from creating books with invalid publication dates.
    
    Meta:
        model: Book - The model this serializer is based on
        fields: '__all__' - Include all fields from the Book model
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields: id, title, publication_year, author
    
    def validate_publication_year(self, value):
        """
        Custom validator for the publication_year field.
        
        This method ensures that the publication year is not in the future.
        It's called automatically during the validation process when creating
        or updating a Book instance through the serializer.
        
        Args:
            value (int): The publication year to validate
        
        Returns:
            int: The validated publication year if valid
        
        Raises:
            serializers.ValidationError: If the publication year is in the future
        
        Example:
            If current year is 2025:
            - validate_publication_year(2024) -> Returns 2024 (valid)
            - validate_publication_year(2026) -> Raises ValidationError (invalid)
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. "
                f"Current year is {current_year}, but got {value}."
            )
        
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer demonstrates advanced DRF features by including a nested
    representation of all books written by the author. The nested serialization
    allows clients to retrieve complete author information including all their
    books in a single API call.
    
    Fields:
        - id: Auto-generated primary key (read-only)
        - name: The author's full name
        - books: A nested list of all books by this author (read-only)
    
    Nested Serialization:
        The 'books' field uses the BookSerializer to serialize all related Book
        instances. This is achieved through:
        1. The related_name='books' on the Book.author ForeignKey field
        2. Setting many=True to serialize multiple book instances
        3. Setting read_only=True since books are managed separately
    
    How the relationship works:
        - When you serialize an Author instance, the serializer automatically
          queries all related Book instances using the reverse relationship
          (author.books.all())
        - Each book is then serialized using the BookSerializer
        - The result is a nested JSON structure with the author's info and
          all their books
    
    Example JSON output:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Harry Potter and the Chamber of Secrets",
                    "publication_year": 1998,
                    "author": 1
                }
            ]
        }
    
    Meta:
        model: Author - The model this serializer is based on
        fields: ['id', 'name', 'books'] - Explicitly list fields to include
    """
    
    # Nested serializer for related books
    # - Uses BookSerializer to serialize each book
    # - many=True because one author can have multiple books
    # - read_only=True because we don't create/update books through the author endpoint
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include id, name, and nested books
