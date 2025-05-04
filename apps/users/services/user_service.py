from django.contrib.auth.models import User

class UserService:
    @staticmethod
    def get_user_profile(user_id):
        return User.objects.get(pk=user_id)
