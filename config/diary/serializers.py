from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from django.contrib.auth import authenticate
from .models import Profile, Diary


# 새로운 Diary 시리얼라이저 추가
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'user', 'created_at', 'emotion1', 'emotion2','emotion3', 'content1', 'content2', 'content3']
        read_only_fields = ['user', 'created_at']
