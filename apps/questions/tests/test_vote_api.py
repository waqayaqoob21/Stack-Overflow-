from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.questions.models.question import Question
from apps.answers.models.answer import Answer
from apps.questions.models.vote import Vote

class VoteAPITestCase(APITestCase):
    def setUp(self):
        self.asker = User.objects.create_user(username='asker', password='pass123')
        self.responder = User.objects.create_user(username='responder', password='pass123')

        # Tokens
        token_res = self.client.post(reverse('token_obtain_pair'), {
            'username': 'responder',
            'password': 'pass123'
        })
        self.token = token_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Question and Answer
        self.question = Question.objects.create(
            title='Vote Question',
            body='Vote question body',
            tags='test,vote',
            author=self.asker
        )
        self.answer = Answer.objects.create(
            question=self.question,
            author=self.responder,
            body='Answer to vote'
        )

    def test_upvote_question(self):
        res = self.client.post(reverse('question-vote', args=[self.question.id]), {'vote_type': 1})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Vote.objects.count(), 1)

    def test_downvote_answer(self):
        res = self.client.post(reverse('answer-vote', args=[self.answer.id]), {'vote_type': -1})
        self.assertEqual(res.status_code, 200)
        vote = Vote.objects.first()
        self.assertEqual(vote.vote_type, -1)

    def test_change_vote(self):
        self.client.post(reverse('question-vote', args=[self.question.id]), {'vote_type': 1})
        self.client.post(reverse('question-vote', args=[self.question.id]), {'vote_type': -1})
        vote = Vote.objects.get(user=self.responder)
        self.assertEqual(vote.vote_type, -1)
        self.assertEqual(Vote.objects.count(), 1)

    def test_remove_vote(self):
        self.client.post(reverse('question-vote', args=[self.question.id]), {'vote_type': 1})
        self.assertEqual(Vote.objects.count(), 1)
        res = self.client.delete(reverse('question-vote', args=[self.question.id]))
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Vote.objects.count(), 0)

    def test_unauthenticated_vote_blocked(self):
        self.client.credentials()  # Remove the token
        res = self.client.post(reverse('question-vote', args=[self.question.id]), {'vote_type': 1})
        self.assertEqual(res.status_code, 401)
