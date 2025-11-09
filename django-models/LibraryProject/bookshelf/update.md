# Update Operation

**Command Used:**
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
'Nineteen Eighty-Four'
# Book title successfully updated and saved in the database.
