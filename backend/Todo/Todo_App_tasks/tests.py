from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

# Create your tests here.
User = get_user_model()
class TaskTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',password='testpass')
        self.client.force_authenticate(user=self.user)
    def test_create_task(self):
        payload = {
            'title': 'Test Task',
            'description': 'Test description',
            'priority': 'Medium'
        }
        response = self.client.post('/api/tasks/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks(self):
        Task.objects.create(user=self.user, title='Task1', priority='Low')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
