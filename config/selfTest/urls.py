from django.urls import path
from selfTest.views import scoreSaveAndGetResult,getSelfTestDate,getCenterInfo

urlpatterns = [
    path('getResult',scoreSaveAndGetResult.as_view()),
    path('getSelfTestDate',getSelfTestDate.as_view()),
    path('getCenterInfo',getCenterInfo.as_view()),
]