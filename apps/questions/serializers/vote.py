from rest_framework import serializers
from apps.questions.models.vote import Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'vote_type', 'object_id', 'content_type']
