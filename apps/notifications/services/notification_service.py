from apps.notifications.models.notification import Notification
# Create your Services here.
class NotificationService:
    @staticmethod
    def notify(user, message):
        Notification.objects.create(user=user, message=message)