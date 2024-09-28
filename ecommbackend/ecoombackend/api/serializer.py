
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .models import MyUserModel , UserAddressModel ,UserAddressModelData
from django.contrib.auth.hashers import make_password




class ProductSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    number = serializers.IntegerField()




class MyUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUserModel
        fields = ['username', 'email', 'password','phone','alternate_phone']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = MyUserModel.objects.create(**validated_data)
        return user


# Serializer for MyUserModel with nested address data
class MyUserModelSerializerData(serializers.ModelSerializer):
     # Nested serializer for addresses

    class Meta:
        model = MyUserModel
        fields = '__all__'


class UserDataSerilizer(serializers.ModelSerializer):
     # Nested serializer for addresses

    class Meta:
        model = MyUserModel
        fields = ["name" ,"email","phone" , "alternate_phone","username"]


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta :
        model = UserAddressModelData
        fields = "__all__"