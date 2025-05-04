from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from apps.questions.models.question import Question

class QuestionAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token_url = reverse('token_obtain_pair')
        self.question_url = reverse('question-list')

        # Get JWT token
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_question(self):
        data = {
            'title': 'How to test Django APIs?',
            'body': 'I want to write API tests for my Stackoverflow project.',
            'tags': 'django,testing'
        }
        response = self.client.post(self.question_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], data['title'])

    def test_list_questions(self):
        Question.objects.create(title="Title 1", body="Body 1", tags="django", author=self.user)
        Question.objects.create(title="Title 2", body="Body 2", tags="python", author=self.user)
        response = self.client.get(self.question_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_tag(self):
        Question.objects.create(title="Tagged", body="Some text", tags="python", author=self.user)
        response = self.client.get(self.question_url + '?tag=python')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_search_by_title(self):
        Question.objects.create(title="Searchable title", body="details", tags="api", author=self.user)
        response = self.client.get(self.question_url + '?search=searchable')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_question(self):
        question = Question.objects.create(title="Old title", body="old", tags="edit", author=self.user)
        url = reverse('question-detail', args=[question.id])
        updated_data = {
            'title': 'Updated title',
            'body': 'Updated body',
            'tags': 'edit'
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated title')

    def test_delete_question(self):
        question = Question.objects.create(title="To be deleted", body="will go", tags="delete", author=self.user)
        url = reverse('question-detail', args=[question.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Question.objects.filter(id=question.id).exists())

    def test_unauthorized_create(self):
        self.client.credentials()  # remove the token
        data = {
            'title': 'No token',
            'body': 'Unauthenticated post',
            'tags': 'security'
        }
        response = self.client.post(self.question_url, data)
        self.assertEqual(response.status_code, 401)
