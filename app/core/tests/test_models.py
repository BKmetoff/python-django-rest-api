from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='user@box.com', password='testpw'):
    """Creates sample user"""

    return get_user_model().objects.create_user(email, password)


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

    def test_new_user_invalid_email(self):
        """Tests validating creating a new user without email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test_pw')

    def test_create_new_superuser(self):
        """Tests creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'superdude@box.com',
            'test_pw'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Tests tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Tag Name'
        )

        self.assertEqual(str(tag), tag.name)
