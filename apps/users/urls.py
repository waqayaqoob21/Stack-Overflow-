# apps/users/urls.py

from django.urls import path
from .views.auth import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    RegisterView
)
from .views.user import UserProfileView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
