from rest_framework import serializers
from .models import Quest,Quest_history

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'

class QuestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest_history
        fields = '__all__'