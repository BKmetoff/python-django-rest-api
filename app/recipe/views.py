from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers


class TagViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manages tags in DB"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagsSerializer

    def get_queryset(self):
        """Returns objects for current authenticated user only"""

        return self.queryset.filter(user=self.request.user).order_by('-name')
