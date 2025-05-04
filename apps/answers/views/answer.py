from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.answers.models.answer import Answer
from apps.answers.serializers.answer import AnswerSerializer
from apps.answers.services.answer_service import AnswerService
from apps.questions.models.question import Question
from apps.notifications.services.notification_service import NotificationService
# Create your views here.
class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Answer.objects.all()

    def perform_create(self, serializer):
        answer = serializer.save(author=self.request.user)
        question = answer.question
        NotificationService.notify(question.author, f"New answer posted to your question: {question.title}")


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        answer = self.get_object()
        question = answer.question

        if question.author != request.user:
            return Response({'error': 'Only question author can accept an answer.'}, status=403)

        # Send notification to the answer's author
        NotificationService.notify(
            answer.author,
            f"🎉 Your answer to '{question.title}' was accepted!"
        )

        AnswerService.accept_answer(answer)
        return Response({'message': 'Answer accepted successfully.'})
