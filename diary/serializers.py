from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        field = ['id', 'user', 'created_at', 'emotion1', 'emotion2', 'emotion3', 'content1', 'content2', 'content3']
        read_only_field = ['user', 'created_at']