from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagsSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):
    """Tests public tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login requirement to view tags"""

        res = self.client.get(TAGS_URL)
        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class PrivateTagsApiTest(TestCase):
    """Tests tags API for authorized users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'dude@box.com',
            'awesomepw'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Tests retrieving tags"""

        Tag.objects.create(user=self.user, name='Test Tag 1')
        Tag.objects.create(user=self.user, name='Test Tag 2')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagsSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Tests returned tags belong to authenticated user only"""

        user2 = get_user_model().objects.create_user(
            'otherdude@box.com',
            'awesomepw'
        )

        Tag.objects.create(user=user2, name='tag of unauthenticated user')

        tag = Tag.objects.create(
            user=self.user,
            name='tag of authenticated user'
        )

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
