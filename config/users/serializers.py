from django.contrib.auth.models import User #장고 기본 유저모델
from django.contrib.auth.password_validation import validate_password #검증
from .models import Profile
from rest_framework import serializers
from rest_framework.authtoken.models import Token #토큰 모델
from rest_framework.validators import UniqueValidator #이메일 중복 방지

from django.contrib.auth import authenticate

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
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':"password fields didn't match"}
            )
        return data
    
    def create(self, validate_data):
        user = User.objects.create_user(
            username = validate_data['username'],
            email = validate_data['email']
        )

        user.set_password(validate_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {'error' : "user not exist"}
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname")

