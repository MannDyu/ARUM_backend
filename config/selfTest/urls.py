from django.urls import path
from selfTest.views import scoreSaveAndGetResult,getSelfTestDate,getCenterInfo,getDistrict

urlpatterns = [
    path('getResult',scoreSaveAndGetResult.as_view()),
    path('getSelfTestDate',getSelfTestDate.as_view()),
    path('getCenterInfo',getCenterInfo.as_view()),
    path('getDistrict',getDistrict.as_view()),
]