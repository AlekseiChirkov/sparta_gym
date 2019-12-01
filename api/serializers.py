from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from .models import *


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'subscription_type', 'time', 'price')


class ProductTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id', 'type_name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'product_type', 'price', 'description')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', '')
        }


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'date_of_birth', 'role')
        read_only_fields = ('email', )


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ('id', 'user', 'subscription_type')


class PaymentSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(source='get_sum', max_value=None, min_value=None, required=False)

    class Meta:
        model = Payment
        fields = ('id', 'user', 'total_price', 'is_it_open', 'products')


class PaymentProductSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(source='get_cost', max_value=None, min_value=None, required=False)

    class Meta:
        model = PaymentProduct
        fields = ('id', 'product', 'count', 'total_price')
