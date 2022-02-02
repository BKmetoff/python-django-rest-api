from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="superdude@box.com",
            password='test_pw'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='dude@box.com',
            password='test_pw',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Tests listing users on user page"""

        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        # the below also asserts the response code is 200
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Tests user edit page"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Tests create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
