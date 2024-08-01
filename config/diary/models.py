from django.db import models
from django.contrib.auth.models import User

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #유저와의 연결
    created_at = models.DateTimeField(auto_now_add=True)  #글 작성 시각
    emoj = models.CharField(max_length=50)  # 이모지
    emotion1 = models.CharField(max_length=100, blank=True, null=True) #감정1
    emotion2 = models.CharField(max_length=100, blank=True, null=True) #감정2
    emotion3 = models.CharField(max_length=100, blank=True, null=True) #감정3
    content1 = models.TextField()  #본문 1
    content2 = models.TextField()  #본문 2
    content3 = models.TextField()  #본문 3