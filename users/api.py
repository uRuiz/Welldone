# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from users.permissions import UserPermission
from users.serializers import UserSerializer, SignupSerializer, FollowUserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.models import Follower


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        """
        Returns SinupSerializer when trying to create a new user
        """
        return SignupSerializer if self.action in ['create', 'update'] else UserSerializer


class FollowUserViewSet(ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        follows = Follower.objects.all().select_related("followed")
        follows = follows.filter(followed=serializer.validated_data.get("followed"), user=self.request.user.id)
        if follows.count() > 0:
            return follows.delete()
        else:
            return serializer.save(user=self.request.user)
