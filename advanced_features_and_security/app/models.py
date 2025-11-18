from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_view", "Can view post"),
            ("can_create", "Can create post"),
            ("can_edit", "Can edit post"),
            ("can_delete", "Can delete post"),
        ]

    def __str__(self):
        return self.title
