from rest_framework import serializers
from .models import Hospital,Self_test,Self_test_result

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class SelfTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Self_test
        fields = '__all__'

class SelfTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Self_test_result
        fields = '__all__'
