from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from task.models import TaskModel

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('create_account')
        self.login_url = reverse('token_obtain_pair')
        self.valid_user_data = {'username': 'testuser','email': 'test@example.com','password': 'TestPass123','confirm_password': 'TestPass123'}

    # Registration Tests
    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    # Password mismatch test
    def test_user_registration_password_mismatch(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['confirm_password'] = 'WrongPass123'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Invalid email format test
    def test_user_registration_email_invalid(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['email'] = 'test-email'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Password length test
    def test_user_registration_password_invalid(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password'] = '1234567' # less than 8 characters
        invalid_data['confirm_password'] = '1234567'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Duplicate username test
    def test_user_registration_duplicate_username(self):
        self.client.post(self.register_url, self.valid_user_data, format='json')
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['email'] = 'another@example.com'
        response = self.client.post(self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Login Tests wuth invalid credentials
    def test_login_with_invalid_credentials(self):
        self.client.post(self.register_url, self.valid_user_data, format='json')
        login_data = {'username': self.valid_user_data['username'],'password': 'WrongPassword123'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Login Tests with valid credentials
    def test_user_login(self):
        self.client.post(self.register_url, self.valid_user_data, format='json')        
        login_data = {'username': self.valid_user_data['username'],'password': self.valid_user_data['password']}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class TaskAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test user1
        self.user = User.objects.create_user(username='testuser',password='TestPass123')
        # Get authentication token
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser','password': 'TestPass123'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create test task
        self.task = TaskModel.objects.create(user=self.user,title='Test Task',description='Test Description')
        self.task_url = reverse('Task_ListCreate')
        self.task_detail_url = reverse('Task_RetrieveUpdateDelete', kwargs={'pk': self.task.pk})

        # create test user 2
        self.user2 = User.objects.create_user(username='user2', password='Pass2')
        response_user2_token = self.client.post(reverse('token_obtain_pair'), {'username': 'user2','password': 'Pass2'}, format='json')
        self.token2 = response_user2_token.data['access']
        self.client2 = APIClient() 
        self.client2.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')

    # Create, List, Retrieve, Update, Delete Tests

    def test_create_task(self):
        data = {'title': 'New Task','description': 'New Description'}
        response = self.client.post(self.task_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskModel.objects.count(), 2)
        self.assertEqual(TaskModel.objects.get(title='New Task').description, 'New Description')

    def test_list_tasks(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 

    def test_retrieve_task(self):
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        updated_data = {'title': 'Updated Task','description': 'Updated Description','completed': True}
        response = self.client.put(self.task_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskModel.objects.get(pk=self.task.pk).title, 'Updated Task')
        self.assertTrue(TaskModel.objects.get(pk=self.task.pk).completed)

    def test_delete_task(self):
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskModel.objects.count(), 0)

    # Unauthorized Access Test
    def test_unauthorized_access(self):
        # Remove authentication credentials
        self.client.credentials()
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Access Control Tests
    def test_user_cannot_retrieve_another_users_task(self):
        response = self.client2.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update and Delete Tests for Access Control
    def test_user_cannot_update_another_users_task(self):
        updated_data = {'title': 'Hacked Title', 'description': 'Should Fail', 'completed': True}
        response = self.client2.put(self.task_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Test Task') 

    def test_user_cannot_delete_another_users_task(self):
        initial_count = TaskModel.objects.count()
        response = self.client2.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        
        # Verify the task still exists
        self.assertEqual(TaskModel.objects.count(), initial_count)

class TaskFilterTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='TestPass123')
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser','password': 'TestPass123'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        TaskModel.objects.create(user=self.user,title='Completed Task1',description='This task is completed1',completed=True)
        TaskModel.objects.create(user=self.user,title='Completed Task2',description='This task is completed2',completed=True)
        TaskModel.objects.create(user=self.user,title='Incomplete Task',description='This task is not completed',completed=False)

    def test_filter_completed_tasks(self):
        response = self.client.get(f"{reverse('Task_ListCreate')}?is_completed=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], 'Completed Task2')

    def test_filter_incomplete_tasks(self):
        response = self.client.get(f"{reverse('Task_ListCreate')}?is_completed=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Incomplete Task')
