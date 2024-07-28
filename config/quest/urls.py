from django.urls import path
from quest.views import RandomQuest,QuestList,UpdateQuestHistory,MonthlyQuestList,SpecificQuestInfo

urlpatterns = [
    path('randomQuest/<str:qs_theme>/',RandomQuest.as_view(), name='random_quest'),
    path('questList',QuestList.as_view(), name='quest_history_list'),
    path('questPerform',UpdateQuestHistory.as_view(), name='update_quest_history'),
    path('monthlyQuestList/<int:year>/<int:month>/',MonthlyQuestList.as_view(), name='monthly_quest_history'),
    path('specificQuestInfo/<int:year>/<int:month>/<int:day>',SpecificQuestInfo.as_view(), name='specific_quest_history'),
]