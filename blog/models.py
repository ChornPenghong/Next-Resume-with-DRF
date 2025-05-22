from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default="This is default content.")
    created_at = models.DateTimeField(auto_now_add=True)
