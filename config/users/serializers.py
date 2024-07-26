from django.contrib.auth.models import User #장고 기본 유저모델
from django.contrib.auth.password_validation import validate_password #검증
from rest_framework import serializers
from rest_framework.authtoken.models import Token #토큰 모델
from rest_framework.validators import UniqueValidator #이메일 중복 방지
from django.contrib.auth import authenticate
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())] #데이터 베이스에 존재하는지 확인
    )

    password = serializers.CharField(
        write_only = True, 
        required = True,
        validators = [validate_password] #비밀번호 유효성 검사
    )

    password2 = serializers.CharField(
        write_only = True, 
        required = True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data): #비밀번호가 일치하는지 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':"password fields didn't match"}
            )
        return data
    
    def create(self, validate_data): #회원가입 성공하면 보이는 요소
        user = User.objects.create_user(
            username = validate_data['username'],
            email = validate_data['email']
        )

        user.set_password(validate_data['password']) #비밀번호 저장
        user.save() #데이터베이스에 저장
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(**data) #authenticate 함수가 인증이 성공되면 토큰 반환
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {'error' : "user not exist"}
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname')
        