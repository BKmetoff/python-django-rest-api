from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the public users api"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Tests creating user after submitting valid payload"""

        payload = {
            "email": "test@box.com",
            "password": "fananas",
            "name": "test"
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_users_exists(self):
        """Tests trying to creating an existing user"""

        payload = {
            "email": "test@box.com",
            "password": "fananas",
        }

        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pasword_length(self):
        """Tests the password is the required length"""

        payload = {
            "email": "test@box.com",
            "password": "fn",
            "name": "test"
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Tests token is created for user"""

        payload = {
            'email': 'user@box.com',
            'password': 'testpass'
        }

        create_user(**payload)

        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Tests tokens are not created when credentials are invalid"""

        create_user(email='user@box.com', password='somepassword')
        payload = {
            'email': 'user@box.com',
            'password': 'otherpassword'
        }

        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Tests token is not created for non-existing user"""

        payload = {
            'email': 'user@box.com',
            'password': 'testpass'
        }

        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Tests email and password are required"""

        response = self.client.post(
            TOKEN_URL,
            {'email': 'some', 'password': ''}
        )

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
