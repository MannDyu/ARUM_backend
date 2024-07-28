from django.urls import path
from .views import DiaryCreateView, DiaryListView, DiaryDetailView, MonthDiaryListView

urlpatterns = [
    path('diary/', DiaryCreateView.as_view(), name="diary_create"),
    path('diary/list/', DiaryListView.as_view(), name="diary_list"),
    path('diary/<int:pk>/', DiaryDetailView.as_view(), name="diary_detail"),
    path('diary/list/month/', MonthDiaryListView.as_view(), name="month_diary_list"),
]