
from django.db import models
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_books'
    )

    class Meta:
        permissions = (
            ("can_create", "Can create book"),
            ("can_delete", "Can delete book"),
        )

    def __str__(self):
        return self.title


# Create your models here.


