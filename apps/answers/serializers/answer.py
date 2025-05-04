from rest_framework import serializers
from apps.answers.models.answer import Answer
# Create your Serializers here.
class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'author', 'body', 'is_accepted', 'created_at', 'updated_at']
        read_only_fields = ['author', 'is_accepted', 'created_at', 'updated_at']
