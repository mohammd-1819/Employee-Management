from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from employee.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserListViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(email='user1@gmail.com', password='user1234')

    def setUp(self):
        # jwt token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_user_list(self):
        url = reverse('employee:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDetailViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(email='user1@gmail.com', password='user1234')

    def setUp(self):
        # JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_user_detail(self):
        url = reverse('employee:user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_detail(self):
        url = reverse('employee:user-detail', args=[self.user.id])
        data = {'email': 'updated_user@gmail.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated_user@gmail.com')

    def test_delete_user(self):
        url = reverse('employee:user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class UserCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def setUp(self):
        self.client.credentials()

    def test_create_user(self):
        url = reverse('employee:user-create')
        data = {
            'email': 'newuser@gmail.com',
            'password': 'newuser1234',
            'username': 'newuser1819',
            'fullname': 'new_user',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@gmail.com').exists())
