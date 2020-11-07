from rest_framework import serializers

from shop.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def create(self, validated_data):
        sub = Subscription.objects.create(
            user=validated_data.get('user'),
        )
        return sub
