from django.urls import path
from .views import DiaryCreateView, DiaryListView, DiaryDetailView, RecentDiaryListView

urlpatterns = [
    path('diary/', DiaryCreateView.as_view(), name='diary_create'),
    path('diary/list/', DiaryListView.as_view(), name='diary_list'),
    path('diary/<int:pk>/', DiaryDetailView.as_view(), name='diary_detail'),
    path('diary/list/recent/', RecentDiaryListView.as_view(), name='recent_diary_list'),
]