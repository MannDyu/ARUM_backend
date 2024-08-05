from django.db import models
from django.contrib.auth.models import User

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #유저와의 연결
    created_at = models.DateTimeField(auto_now_add=True)  #글 작성 시각
    feel = models.CharField(max_length=50, default='default_value') #기분
    emotion = models.CharField(max_length=50)  #메인 감정
    tag1 = models.CharField(max_length=100, blank=True, null=True) #태그1
    tag2 = models.CharField(max_length=100, blank=True, null=True) #태그2
    tag3 = models.CharField(max_length=100, blank=True, null=True) #태그3
    content1 = models.TextField()  #본문 1
    content2 = models.TextField()  #본문 2
    content3 = models.TextField()  #본문 3