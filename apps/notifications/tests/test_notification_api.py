from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.questions.models.question import Question
from apps.answers.models.answer import Answer
from apps.notifications.models.notification import Notification

class NotificationAPITest(APITestCase):
    def setUp(self):
        self.asker = User.objects.create_user(username='asker', password='askpass')
        self.answerer = User.objects.create_user(username='answerer', password='anspass')

        self.asker_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'asker',
            'password': 'askpass'
        }).data['access']

        self.answerer_token = self.client.post(reverse('token_obtain_pair'), {
            'username': 'answerer',
            'password': 'anspass'
        }).data['access']

        self.question = Question.objects.create(
            title='Notify me?',
            body='Does it notify?',
            tags='notify',
            author=self.asker
        )

    def test_notification_on_answer_creation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.answerer_token}')
        self.client.post(reverse('answer-list'), {
            'question': self.question.id,
            'body': 'Yes, it does notify!'
        })

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.asker_token}')
        res = self.client.get('/api/notifications/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('results', res.data)
        results = res.data["results"]
        self.assertEqual(len(results), 1)
        self.assertIn('New answer posted', results[0]['message'])

    def test_notification_on_answer_acceptance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.answerer_token}')
        ans = self.client.post(reverse('answer-list'), {
            'question': self.question.id,
            'body': 'Will this be accepted?'
        }).data

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.asker_token}')
        self.client.post(reverse('answer-accept', args=[ans['id']]))

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.answerer_token}')
        res = self.client.get('/api/notifications/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('results', res.data)
        results = res.data["results"]
        self.assertEqual(len(results), 1)
        self.assertIn('was accepted', results[0]['message'])

    def test_unauthorized_user_blocked(self):
        self.client.credentials()  # No token
        res = self.client.get('/api/notifications/')
        self.assertEqual(res.status_code, 401)

    def test_notifications_order(self):
        Notification.objects.create(user=self.asker, message="First")
        Notification.objects.create(user=self.asker, message="Second")

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.asker_token}')
        res = self.client.get('/api/notifications/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('results', res.data)

        results = res.data["results"]
        messages = [n["message"] for n in results]
        self.assertEqual(messages[0], "Second")
        self.assertEqual(messages[1], "First")

    def test_mark_notification_as_read(self):
        notif = Notification.objects.create(user=self.asker, message="Unread notification")

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.asker_token}')
        res = self.client.patch(reverse('notification-read', args=[notif.id]))
        self.assertEqual(res.status_code, 200)
        self.assertIn('message', res.data)

        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
