from rest_framework import serializers
from apps.notifications.models.notification import Notification
# Create your Serializers here.
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
