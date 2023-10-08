from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from online_school.permissions import IsModerator, IsSuperUser
from users.models import User
from users.serializers import UsersSerializer, UserCreateSerializer
from django.contrib.auth.models import update_last_login


# Create your views here.
class UsersListAPIView(generics.ListAPIView):
    """
    Эндпоинт для спискового отображения пользователей
    """
    # permission_classes = [IsAuthenticated,  IsModerator | IsSuperUser]
    serializer_class = UsersSerializer
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания пользователя
    """
    # permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = UsersSerializer


class UserUpdateAPIVIew(generics.UpdateAPIView):
    """
    Эндпоинт для обновления пользователя
    """
    # permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UsersRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт для просмотра конкретного пользователя
    """
    # permission_classes = [IsAuthenticated,  IsModerator | IsSuperUser]
    serializer_class = UsersSerializer
    queryset = User.objects.all()
