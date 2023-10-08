from online_school.apps import OnlineSchoolConfig
from rest_framework.routers import DefaultRouter
from online_school.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDeleteAPIView, PaymentCreateAPIView, PaymentListAPIView, PaymentDeleteAPIView, \
    SubscriptionCreateAPIView, SubscriptionDeleteAPIView, SubscriptionUpdateAPIView, SubscriptionListAPIView
from django.urls import path


app_name = OnlineSchoolConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_delete'),

    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('payments/delete/<int:pk>/', PaymentDeleteAPIView.as_view(), name='payment_delete'),

    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDeleteAPIView.as_view(), name='subscription_delete'),
    path('subscriptions/update/<int:pk>/', SubscriptionUpdateAPIView.as_view(), name='subscription_update'),
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscriptions'),
              ] + router.urls
