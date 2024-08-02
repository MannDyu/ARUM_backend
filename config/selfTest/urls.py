from django.urls import path
from selfTest.views import scoreSaveAndGetResult,getSelfTestDate,getDefaultCenterInfo

urlpatterns = [
    path('getResult',scoreSaveAndGetResult.as_view()),
    path('getSelfTestDate',getSelfTestDate.as_view()),
    path('getDefaultCenterInfo',getDefaultCenterInfo.as_view()),
]