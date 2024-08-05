from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'user', 'created_at', 'feel','emotion', 'tag1', 'tag2', 'tag3', 'content1', 'content2', 'content3']
        read_only_fields = ['user', 'created_at']

class FeelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['created_at', 'feel']