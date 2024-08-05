from django.urls import path
from .views import DiaryCreateView, DiaryDetailView, MonthDiaryListView,  FeelRatioView, FeelCalendarDiaryView, CheckTodayDiaryView

urlpatterns = [
    path('', DiaryCreateView.as_view(), name='diary_create'), #일기 생성
    path('<int:pk>/', DiaryDetailView.as_view(), name='diary_detail'), #일기 조회,수정,삭제
    path('list/month/', MonthDiaryListView.as_view(), name='diary_list_month'), #한 달 일기 목록
    path('feel/calendar/', FeelCalendarDiaryView.as_view(), name='diary_feel_calendar'), #한 달 기분 목록(달력)
    path('check/', CheckTodayDiaryView.as_view(), name="diary_yn_check"), #일기 작성 여부
    path('feel/ratio/', FeelRatioView.as_view(), name='diary_feel_ratio'), #일기 기분 통계
]