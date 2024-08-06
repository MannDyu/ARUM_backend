from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password 
from .models import Profile
from rest_framework import serializers
from rest_framework.authtoken.models import Token 
from rest_framework.validators import UniqueValidator 
from django.contrib.auth import authenticate

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
        token = Token.objects.create(user=user)  # 사용자 생성 후 토큰 생성
        return user

#로그인
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    # def validate(self, data):
    #     user = authenticate(**data)
    #     if user:
    #         token = Token.objects.get(user=user)
    #         return token
    #     raise serializers.ValidationError(
    #         {'error' : "user not exist"}
    #     )
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return {
                'token': token.key,
                'username': user.username
            }
        raise serializers.ValidationError({'error': "Invalid credentials"})

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
    


