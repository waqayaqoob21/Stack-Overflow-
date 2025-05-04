from rest_framework import serializers
from apps.questions.models.question import Question

class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'tags', 'tag_list', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at', 'tag_list']
