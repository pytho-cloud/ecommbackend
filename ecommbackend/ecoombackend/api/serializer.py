
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .models import MyUserModel , UserAddressModel
from django.contrib.auth.hashers import make_password




class ProductSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    number = serializers.IntegerField()




class MyUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUserModel
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = MyUserModel.objects.create(**validated_data)
        return user

class UserAddressModelSerializer(serializers.ModelSerializer):
    user = MyUserModelSerializer(read_only=True)
    
    class Meta:
        model = UserAddressModel
        fields = ['user', 'address', 'last_update']