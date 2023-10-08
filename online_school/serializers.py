from rest_framework import serializers
from online_school.models import Course, Lesson, Payment, Subscription
from online_school.validators import VideoLinkValidator
import stripe
stripe.api_key = 'sk_test_51NrIuYEr4bPb9axLqE4JA5i65jeKiqFMIenTkPJpqY8e2ngTKGjrpl5I4pEq5V1iTB2yiFP3TuImcneVz6k3461u00Ifn7stOf'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'course', 'user', 'is_active']


class SubscriptionSerializerForList(serializers.ModelSerializer):
    course = serializers.SlugRelatedField('name', read_only=True)
    user = serializers.SlugRelatedField('email', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'course', 'user', 'is_active']


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    subscribed_users = serializers.SerializerMethodField()

    # @staticmethod
    # def get_count_lessons(obj):
    #     return obj.lesson_set.count()

    @staticmethod
    def get_subscribed_users(obj):
        queryset = obj.subscriptions.filter(is_active=True)
        serializer = SubscriptionSerializer(instance=queryset, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'added_by', 'count_lessons', 'lessons', 'subscribed_users']


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        product = stripe.Product.create(name=validated_data['course'].name)
        price = stripe.Price.create(unit_amount=validated_data['sum_of_payment'], currency="usd",
                                    recurring={"interval": "month"}, product=product['id'])
        checkout = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price": price['id'],
                    "quantity": 1,
                },
            ],
            mode="subscription",
        )
        validated_data['payment_url'] = checkout['url']
        payment = Payment.objects.create(**validated_data)

        return payment




