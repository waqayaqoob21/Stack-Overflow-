from apps.questions.models.vote import Vote
from django.contrib.contenttypes.models import ContentType

class VoteService:
    @staticmethod
    def vote(user, model_instance, vote_type):
        content_type = ContentType.objects.get_for_model(model_instance)
        vote, created = Vote.objects.update_or_create(
            user=user,
            content_type=content_type,
            object_id=model_instance.id,
            defaults={'vote_type': vote_type}
        )
        return vote

    @staticmethod
    def unvote(user, model_instance):
        content_type = ContentType.objects.get_for_model(model_instance)
        Vote.objects.filter(
            user=user,
            content_type=content_type,
            object_id=model_instance.id
        ).delete()
