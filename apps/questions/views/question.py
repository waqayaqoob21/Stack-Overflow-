from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from apps.questions.models.question import Question
from apps.questions.serializers.question import QuestionSerializer
from apps.questions.services.question_service import QuestionService

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Question.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = QuestionService.get_all_questions()
        tag = self.request.query_params.get('tag')
        search = self.request.query_params.get('search')

        if tag:
            queryset = QuestionService.filter_by_tag(tag)
        if search:
            queryset = QuestionService.search_by_title(search)

        return queryset
