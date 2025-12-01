from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    This model stores basic information about authors who have written books.
    Each author can have multiple books associated with them through a 
    one-to-many relationship (one author can write many books).
    
    Fields:
        name (CharField): The full name of the author. Limited to 100 characters.
    
    Methods:
        __str__: Returns the author's name for easy identification in admin and shell.
    """
    name = models.CharField(
        max_length=100,
        help_text="The full name of the author"
    )
    
    def __str__(self):
        """Return the author's name as the string representation."""
        return self.name
    
    class Meta:
        ordering = ['name']  # Order authors alphabetically by name
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model representing a published book.
    
    This model stores information about books and establishes a relationship
    with the Author model. Each book is written by one author (many-to-one 
    relationship from Book to Author).
    
    Fields:
        title (CharField): The title of the book. Limited to 200 characters.
        publication_year (IntegerField): The year the book was published.
            This field will be validated by the serializer to ensure it's not
            in the future.
        author (ForeignKey): A foreign key relationship to the Author model.
            When an author is deleted, all their books are also deleted (CASCADE).
            The related_name='books' allows reverse lookup from Author to Books.
    
    Methods:
        __str__: Returns the book title for easy identification in admin and shell.
    
    Relationships:
        - Many-to-One with Author: Multiple books can belong to one author.
        - The related_name='books' on the author field allows accessing all books
          of an author using author_instance.books.all()
    """
    title = models.CharField(
        max_length=200,
        help_text="The title of the book"
    )
    
    publication_year = models.IntegerField(
        help_text="The year the book was published"
    )
    
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  # Delete books when author is deleted
        related_name='books',  # Allows reverse lookup: author.books.all()
        help_text="The author who wrote this book"
    )
    
    def __str__(self):
        """Return the book title as the string representation."""
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        ordering = ['-publication_year', 'title']  # Order by year (newest first), then title
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
