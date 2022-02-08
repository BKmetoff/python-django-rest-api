from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


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
