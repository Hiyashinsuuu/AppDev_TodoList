# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import todo
import re

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = todo
        fields = ['id', 'user', 'todo_name', 'status']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data['password']
        self.validate_password(password)  # Call the password validation method

        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(password)  # Hash the password
        user.save()
        return user

    def validate_password(self, password):
        special_characters = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]"
        
        if len(password) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        elif not re.search(r'[A-Z]', password):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        elif not re.search(r'[a-z]', password):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        elif not re.search(r'\d', password):
            raise serializers.ValidationError('Password must contain at least one number.')
        elif not re.search(special_characters, password):
            raise serializers.ValidationError('Password must contain at least one special character.')

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()