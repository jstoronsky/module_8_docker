from users.apps import UsersConfig
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from django.urls import path
from users.views import UsersListAPIView, UsersRetrieveAPIView, UserCreateAPIView, UserUpdateAPIVIew

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UsersListAPIView.as_view(), name='users'),
    path('<int:pk>/', UsersRetrieveAPIView.as_view(), name='user_detail'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateAPIVIew.as_view(), name='user_update')
]
