from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import DiarySerializer, FeelSerializer
from .models import Diary
from collections import Counter
from django.utils import timezone

#생성
class DiaryCreateView(generics.CreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#조회,수정,삭제
class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    #queryset을 재정의하여 인증된 사용자의 다이어리 항목만 반환
    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

#한 달 일기 목록
class MonthDiaryListView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        start_of_month = make_aware(datetime(now.year, now.month, 1))
        end_of_month = make_aware(datetime(now.year, now.month + 1, 1)) if now.month < 12 else make_aware(datetime(now.year + 1, 1, 1))
        return Diary.objects.filter(user=self.request.user, created_at__range=(start_of_month, end_of_month))

#한 달 기분 목록(달력)
class FeelCalendarDiaryView(generics.ListAPIView):
    serializer_class = FeelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        start_of_month = make_aware(datetime(now.year, now.month, 1))
        end_of_month = make_aware(datetime(now.year, now.month + 1, 1)) if now.month < 12 else make_aware(datetime(now.year + 1, 1, 1))
    
        return Diary.objects.filter(user=self.request.user, created_at__range=(start_of_month, end_of_month)).values('created_at','feel')

#일기 작성 여부
class CheckTodayDiaryView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = timezone.now().date()
        return Diary.objects.filter(created_at__date=now, user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            return Response({"diary_yn": True}) #작성함
        else:
            return Response({"diary_yn": False}) #작성하지 않음

#한 달 기분 통계
class FeelRatioView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        start_of_month = make_aware(datetime(now.year, now.month, 1))
        end_of_month = make_aware(datetime(now.year, now.month + 1, 1)) if now.month < 12 else make_aware(datetime(now.year + 1, 1, 1))
        return Diary.objects.filter(user=self.request.user, created_at__range=(start_of_month, end_of_month))

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        feel_descriptions = {
            '아주 좋아요': 0,
            '좋아요': 0,
            '괜찮아요': 0,
            '나빠요': 0,
            '아주 나빠요': 0
        }

        feels = [diary.feel for diary in queryset if diary.feel]
        
        if feels:
            feels_count = Counter(feels)
            total_count = sum(feels_count.values())

            for feel, count in feels_count.items():
                if feel in feel_descriptions:
                    feel_descriptions[feel] += count

            feel_ratios = {feel: (count / total_count) * 100 for feel, count in feel_descriptions.items()}
        else:
            feel_ratios = {feel: 0 for feel in feel_descriptions.keys()}

        return Response(feel_ratios)