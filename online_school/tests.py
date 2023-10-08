from rest_framework.test import APITestCase
from rest_framework import status
from online_school.models import Lesson, Subscription, Course
from users.models import User
# Create your tests here.


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_lesson(self):
        """
        тест создания уроков
        """
        data = {
            "name": "Lessssson",
            "description": "This is lesssssooon",
        }
        response = self.client.post(
            "/lesson/create/",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {'id': 1, 'name': 'Lessssson', 'preview': None, 'description': 'This is lesssssooon',
                          'video_link': None, 'course': None, 'added_by': None}
                         )
        self.assertTrue(Lesson.objects.all().count() > 0)

    def test_list_lesson(self):
        """
        тест вывода списка уроков
        """

        Lesson.objects.create(name='Less', description='This is less')
        response = self.client.get(
            '/lessons/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'count': 1, 'next': None, 'previous': None, 'results':
                             [{'id': 2, 'name': 'Less', 'preview': None, 'description': 'This is less',
                               'video_link': None, 'course': None, 'added_by': None}]}
                         )

    def test_update_lesson(self):
        """
        тест обновления урока
        """
        Lesson.objects.create(name='Less', description='This is less')

        data = {
            'name': 'More',
            'description': 'There is more interesting'
        }

        response = self.client.patch(
            '/lesson/update/3/',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'id': 3, 'name': 'More', 'preview': None, 'description': 'There is more interesting',
                          'video_link': None, 'course': None, 'added_by': None}
                         )

        self.client.delete(
            '/lesson/delete/3/',
        )

        queryset = Lesson.objects.all()
        self.assertTrue(len(queryset) == 0)

    def tearDown(self):
        Lesson.objects.all().delete()
        return super().tearDown()


class SubscriptionTest(APITestCase):
    def setUp(self) -> None:
        pass

    def test_create_subscription(self):
        Course.objects.create(name='Less', description='This is less')
        User.objects.create(email='adasda@test.com', password='tgbyhnujm')
        data = {
            'course': 1,
            'user': 1,
            'is_active': True
        }

        response = self.client.post('/subscription/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        subscription = Subscription.objects.get(pk=1)
        user = User.objects.get(pk=1)

        self.assertEqual(subscription.course.name, 'Less')
        self.assertEqual(subscription.user.email, 'adasda@test.com')
        self.assertTrue(user.subscriptions.get(course=1).is_active)

    def tearDown(self):
        Course.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()
