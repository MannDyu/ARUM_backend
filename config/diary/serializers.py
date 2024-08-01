from rest_framework import serializers
from .models import Diary


# 새로운 Diary 시리얼라이저 추가
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'user', 'created_at', 'emoj', 'emotion1', 'emotion2','emotion3', 'content1', 'content2', 'content3']
        read_only_fields = ['user', 'created_at']
