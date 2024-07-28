from django.shortcuts import render
from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import DiarySerializer
from .models import Diary

# 새로운 Diary 뷰 추가
class DiaryCreateView(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DiaryListView(generics.ListAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

class MonthDiaryListView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        start_of_month = make_aware(datetime(now.year, now.month, 1))
        end_of_month = make_aware(datetime(now.year, now.month + 1, 1)) if now.month < 12 else make_aware(datetime(now.year + 1, 1, 1))
        return Diary.objects.filter(user=self.request.user, created_at__range=(start_of_month, end_of_month))