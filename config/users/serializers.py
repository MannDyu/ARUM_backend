import jwt
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password 
from .models import Profile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import RefreshTokenModel
from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenObtainSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, get_object_or_404

#회원가입
class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only = True, 
        required = True,
        validators = [validate_password]
    )

    password2 = serializers.CharField(
        write_only = True, 
        required = True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        username = data.get('username', None)
        #username이 이미 존재한다면,
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("user already exists")
        #비민번호가 일치하지 않는다면,
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':"password fields didn't match"}
            )
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

#로그인
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if User.objects.filter(username=username).exists():
            if not user.check_password(password):
                raise serializers.ValidationError('password:"wrong password"')
        else:
            raise serializers.ValidationError("user account not exist")

        token = TokenObtainPairSerializer.get_token(user) #refresh토큰 생성
        refresh_token = str(token)
        access_token = str(token.access_token) #access토큰 생성

        expires_at = timezone.now() + settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')

        RefreshTokenModel.objects.update_or_create(
            user=user,
            defaults={
                'refresh_token': refresh_token,
                'expires_at': expires_at
            }            
        )

        response = Response(
            {
                "user": user.username,
                "message": "login success",
                "jwt_token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            },
            status=status.HTTP_200_OK
        )

        return response

#프로필
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    new_password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = Profile
        fields = ("username","new_password","nickname")
    
    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)

        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()

        if new_password:
            instance.user.set_password(new_password)
            instance.user.save()

        return instance
