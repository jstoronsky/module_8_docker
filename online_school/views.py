from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticated
from online_school.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, \
    SubscriptionSerializer, SubscriptionSerializerForList, PaymentCreateSerializer
from online_school.models import Course, Lesson, Payment, Subscription
from online_school.permissions import IsModerator, IsSuperUser, IsOwner
from online_school.paginators import LessonPaginator, CoursePaginator
import stripe
from online_school.tasks import send_updated_info

stripe.api_key = 'sk_test_51NrIuYEr4bPb9axLqE4JA5i65jeKiqFMIenTkPJpqY8e2ngTKGjrpl5I4pEq5V1iTB2yiFP3TuImcneVz6k3461u00Ifn7stOf'


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def create(self, request, *args, **kwargs):
        """
        Эндпоинт для создания курса
        """
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Эндпоинт для спискового отображения курсов
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Эндпоинт для просмотра конктретного курса
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Эндпоинт для обновления курса
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Эндпоинт для обновления курса
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Эндпоинт для удаления курса
        """
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        course = serializer.save()
        send_updated_info.delay(course.pk)

    # def get_permissions(self):
    #     if self.action == 'list':
    #         pass
    #         self.permission_classes = [IsAuthenticated]
    #
    #     elif self.action in ['retrieve', 'update', 'partial_update']:
    #         self.permission_classes = [IsAuthenticated,  IsModerator | IsSuperUser | IsOwner]
    #
    #     elif self.action == 'create':
    #         self.permission_classes = [IsAuthenticated, ~IsModerator]
    #
    #     elif self.action == 'destroy':
    #         self.permission_classes = [IsAuthenticated, IsSuperUser]
    #
    #     return super(CourseViewSet, self).get_permissions()


class LessonListAPIView(generics.ListAPIView):
    """
    Эндпоинт для спискового отображения уроков
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт для просмотра конктретного урока
    """
    permission_classes = [IsAuthenticated,  IsModerator | IsSuperUser | IsOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания урока
    """
    # permission_classes = [IsAuthenticated, ~IsModerator]
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для обновления урока
    """
    # permission_classes = [IsAuthenticated,  IsModerator | IsSuperUser | IsOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDeleteAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления урока
    """
    # permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Lesson.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания платежа
    """
    # permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = PaymentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'Данные по платежу': serializer.data},
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class PaymentListAPIView(generics.ListAPIView):
    """
    Эндпоинт для спискового отображения платежей
    """
    # permission_classes = [IsAuthenticated,  IsModerator | IsSuperUser]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, rest_framework.DjangoFilterBackend]
    ordering_fields = ['date_of_payment']
    filterset_fields = ['course', 'payment_method']


class PaymentDeleteAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления платежа
    """
    # permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Payment.objects.all()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания подписки
    """
    serializer_class = SubscriptionSerializer


class SubscriptionListAPIView(generics.ListAPIView):
    """
    Эндпоинт для спискового отображения подписок
    """
    serializer_class = SubscriptionSerializerForList
    queryset = Subscription.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для обновления подписки
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления подписки
    """
    queryset = Subscription.objects.all()
