from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import DiarySerializer
from .models import Diary


#생성
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

    #queryset을 재정의하여 인증된 사용자의 다이어리 항목만 반환
    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

#조회,수정,삭제
class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    #queryset을 재정의하여 인증된 사용자의 다이어리 항목만 반환
    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

class RecentDiaryListView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        start_of_month = make_aware(datetime(now.year, now.month, 1))
        end_of_month = make_aware(datetime(now.year, now.month + 1, 1)) if now.month < 12 else make_aware(datetime(now.year + 1, 1, 1))
        return Diary.objects.filter(user=self.request.user, created_at__range=(start_of_month, end_of_month))
