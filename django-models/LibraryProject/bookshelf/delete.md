# Delete Operation

**Command Used:**
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()

(1, {'bookshelf.Book': 1})
<QuerySet []>
# The book instance was successfully deleted and the table is now empty.
