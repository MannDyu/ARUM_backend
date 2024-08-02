from django.urls import path
from quest.views import RandomQuest,QuestList,UpdateQuestHistory,MonthlyQuestList,SpecificQuestInfo,CheckQuestCreatedToday,PerformTodayQuestYN,CheckQuestCreationAndPerformanceToday

urlpatterns = [
    # path('randomQuest/<str:qs_theme>/',RandomQuest.as_view(), name='random_quest'),
    path('randomQuest',RandomQuest.as_view(), name='random_quest'),
    path('questList',QuestList.as_view(), name='quest_history_list'),
    path('questPerform',UpdateQuestHistory.as_view(), name='update_quest_history'),
    path('monthlyQuestList',MonthlyQuestList.as_view(), name='monthly_quest_history'),
    path('specificQuestInfo',SpecificQuestInfo.as_view(), name='specific_quest_history'),
    path('checkQuestCreatedToday',CheckQuestCreatedToday.as_view(), name='quest_created_today_yn'),
    path('checkQuestPerformToday',PerformTodayQuestYN.as_view(), name='quest_perform_today_yn'),
    path('checkQuestCreatePerformToday',CheckQuestCreationAndPerformanceToday.as_view(), name='quest_create_perform_today_yn'),
]