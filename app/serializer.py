from rest_framework import serializers
from . models import *


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ['employee', 'department']
        

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['ID', 'first_name', 'last_name', 'email', 'phone_number', 'biography', 'avatar_url', 'page_count', 'font_size', 'font_style', 'hashed_password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user