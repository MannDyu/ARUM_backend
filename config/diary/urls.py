from django.urls import path
from .views import DiaryCreateView, DiaryDetailView, MonthDiaryListView,  EmojRatioView, CheckTodayDiaryView

urlpatterns = [
    path('', DiaryCreateView.as_view(), name='diary_create'), #일기 생성
    path('<int:pk>/', DiaryDetailView.as_view(), name='diary_detail'), #일기 조회,수정,삭제
    path('list/month/', MonthDiaryListView.as_view(), name='diary_list_month'), #한 달 일기 목록
    path('check/', CheckTodayDiaryView.as_view(), name="diary_yn_check"), #일기 작성 여부
    path('emoj/ratio/', EmojRatioView.as_view(), name='diary_emoj_ratio'), #일기 이모지 통계
]