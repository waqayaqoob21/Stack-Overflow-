from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.questions.services.vote_service import VoteService
from apps.questions.models.question import Question
from apps.answers.models.answer import Answer

class QuestionVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        vote_type = int(request.data.get('vote_type'))  # 1 or -1
        question = Question.objects.get(pk=pk)
        VoteService.vote(request.user, question, vote_type)
        return Response({'message': 'Vote submitted'})

    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        VoteService.unvote(request.user, question)
        return Response({'message': 'Vote removed'}, status=204)

class AnswerVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        vote_type = int(request.data.get('vote_type'))  # 1 or -1
        from apps.answers.models.answer import Answer
        answer = Answer.objects.get(pk=pk)
        VoteService.vote(request.user, answer, vote_type)
        return Response({'message': 'Vote submitted'})

    def delete(self, request, pk):
        from apps.answers.models.answer import Answer
        answer = Answer.objects.get(pk=pk)
        VoteService.unvote(request.user, answer)
        return Response({'message': 'Vote removed'}, status=204)
