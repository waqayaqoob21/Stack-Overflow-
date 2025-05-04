from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.questions.views.question import QuestionViewSet
from apps.questions.views.vote import QuestionVoteView, AnswerVoteView

# ViewSet router for questions
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')

# Add router.urls to urlpatterns
urlpatterns = router.urls

# Add custom endpoints for voting
urlpatterns += [
    # Question voting endpoint (upvote/downvote/delete)
    path('questions/<int:pk>/vote/', QuestionVoteView.as_view(), name='question-vote'),

    # Answer voting endpoint (note: this view still belongs under questions app logically)
    path('answers/<int:pk>/vote/', AnswerVoteView.as_view(), name='answer-vote'),
]
