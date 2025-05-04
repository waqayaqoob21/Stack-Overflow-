from django.db import models
from django.contrib.auth.models import User
from apps.questions.models.question import Question
from django.contrib.contenttypes.fields import GenericRelation
from apps.questions.models.vote import Vote
# Register your models here.
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    votes = GenericRelation(Vote)

    def __str__(self):
        return f'Answer by {self.author.username} on {self.question.title}'
