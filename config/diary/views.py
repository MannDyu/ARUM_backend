from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import DiarySerializer, EmojiSerializer
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

#한 달 이모지 목록(달력)
class EmojCalendarDiaryView(generics.ListAPIView):
    serializer_class = EmojiSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        start_of_month = make_aware(datetime(now.year, now.month, 1))
        end_of_month = make_aware(datetime(now.year, now.month + 1, 1)) if now.month < 12 else make_aware(datetime(now.year + 1, 1, 1))
    
        return Diary.objects.filter(user=self.request.user, created_at__range=(start_of_month, end_of_month)).values('created_at','emoj')

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

#한 달 이모지 통계
class EmojRatioView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = datetime.now()
        start_of_month = make_aware(datetime(now.year, now.month, 1))
        end_of_month = make_aware(datetime(now.year, now.month + 1, 1)) if now.month < 12 else make_aware(datetime(now.year + 1, 1, 1))
        return Diary.objects.filter(user=self.request.user, created_at__range=(start_of_month, end_of_month))

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        emoji_descriptions = {
            '아주 좋음': 0,
            '좋음': 0,
            '보통': 0,
            '나쁨': 0,
            '아주 나쁨': 0
        }

        emojs = [diary.emoj for diary in queryset if diary.emoj]
        
        if emojs:
            emojs_count = Counter(emojs)
            total_count = sum(emojs_count.values())

            for emoji, count in emojs_count.items():
                if emoji in emoji_descriptions:
                    emoji_descriptions[emoji] += count

            emoj_ratios = {emoji: (count / total_count) * 100 for emoji, count in emoji_descriptions.items()}
        else:
            emoj_ratios = {emoji: 0 for emoji in emoji_descriptions.keys()}

        return Response(emoj_ratios)