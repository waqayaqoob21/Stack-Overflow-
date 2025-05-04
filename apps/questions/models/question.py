from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from apps.questions.models.vote import Vote
# Register your models here.
class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.CharField(max_length=255, help_text="Comma-separated tags")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    votes = GenericRelation(Vote)

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return self.title
