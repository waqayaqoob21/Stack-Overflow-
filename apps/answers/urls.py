from rest_framework.routers import DefaultRouter
from apps.answers.views.answer import AnswerViewSet

router = DefaultRouter()
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = router.urls
