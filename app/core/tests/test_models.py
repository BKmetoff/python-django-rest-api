from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successfull(self):
        """Tests creating a new user with an email"""
        email = 'user@box.com'
        password = 'test_pw'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests normalizing emails of new users"""
        email = 'dude@BOX.COM'
        user = get_user_model().objects.create_user(email, 'test_pw')

        self.assertEqual(user.email, email.lower())
