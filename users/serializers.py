from rest_framework import serializers
from online_school.serializers import PaymentSerializer, SubscriptionSerializer
from users.models import User
from online_school.models import Subscription


class UsersSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'city', 'phone_number', 'payments', 'subscriptions']


class UserCreateSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'city', 'phone_number', 'subscriptions']

    def create(self, validated_data):
        subscriptions_data = validated_data.pop('subscriptions')
        user = User.objects.create(**validated_data)
        for subs in subscriptions_data:
            Subscription.objects.create(**subs, user=user)

        return user

    def update(self, instance, validated_data):
        subscriptions_data = validated_data.pop('subscriptions')
        subscriptions = list(instance.subscriptions.all())
        for subs in subscriptions_data:
            if len(subscriptions) == 0:
                Subscription.objects.create(**subs, user=instance)
            else:
                subscription = subscriptions.pop(0)
                subscription.course = subs.get('course', subscription.course)
                subscription.is_active = subs.get('is_active', subscription.is_active)
                subscription.save()
        instance.save()

        return instance
