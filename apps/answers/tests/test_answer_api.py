from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from apps.questions.models.question import Question
from apps.answers.models.answer import Answer
# Creates your tests here.
class AnswerAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.question_owner = User.objects.create_user(username='asker', password='pass123')
        self.answerer = User.objects.create_user(username='responder', password='pass123')
        self.other_user = User.objects.create_user(username='other', password='pass123')

        # Create token for answerer
        token_res = self.client.post(reverse('token_obtain_pair'), {
            'username': 'responder',
            'password': 'pass123'
        })
        self.answerer_token = token_res.data['access']

        # Create token for question_owner
        token_res2 = self.client.post(reverse('token_obtain_pair'), {
            'username': 'asker',
            'password': 'pass123'
        })
        self.asker_token = token_res2.data['access']

        # Create a question
        self.question = Question.objects.create(
            title='Test Question',
            body='This is a test question.',
            tags='test,answer',
            author=self.question_owner
        )

    def test_create_answer(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.answerer_token}')
        res = self.client.post(reverse('answer-list'), {
            'question': self.question.id,
            'body': 'This is an answer.'
        })
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['body'], 'This is an answer.')

    def test_list_answers(self):
        Answer.objects.create(question=self.question, author=self.answerer, body='Test A1')
        Answer.objects.create(question=self.question, author=self.answerer, body='Test A2')
        res = self.client.get(reverse('answer-list'))
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 2)

    def test_update_answer(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.answerer_token}')
        answer = Answer.objects.create(question=self.question, author=self.answerer, body='Old Body')
        res = self.client.put(reverse('answer-detail', args=[answer.id]), {
            'question': self.question.id,
            'body': 'Updated Body'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['body'], 'Updated Body')

    def test_delete_answer(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.answerer_token}')
        answer = Answer.objects.create(question=self.question, author=self.answerer, body='To delete')
        res = self.client.delete(reverse('answer-detail', args=[answer.id]))
        self.assertEqual(res.status_code, 204)

    def test_accept_answer_by_question_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.asker_token}')
        answer = Answer.objects.create(question=self.question, author=self.answerer, body='Accept me')
        res = self.client.post(reverse('answer-accept', args=[answer.id]))
        self.assertEqual(res.status_code, 200)
        self.assertIn('message', res.data)
        answer.refresh_from_db()
        self.assertTrue(answer.is_accepted)

    def test_accept_answer_by_other_user_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.answerer_token}')
        answer = Answer.objects.create(question=self.question, author=self.answerer, body='Attempt me')
        res = self.client.post(reverse('answer-accept', args=[answer.id]))
        self.assertEqual(res.status_code, 403)

    def test_unauthenticated_create_forbidden(self):
        self.client.credentials()  # No auth token
        res = self.client.post(reverse('answer-list'), {
            'question': self.question.id,
            'body': 'No token body'
        })
        self.assertEqual(res.status_code, 401)
