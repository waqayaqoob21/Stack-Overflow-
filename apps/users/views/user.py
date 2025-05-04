from rest_framework import permissions, generics
from apps.users.serializers.user import UserSerializer
from apps.users.services.user_service import UserService

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserService.get_user_profile(self.request.user.id)
