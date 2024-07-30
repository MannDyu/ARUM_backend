from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저와의 연결
    created_at = models.DateTimeField(auto_now_add=True)  # 글 작성 시각
    diary_yn = models.BooleanField(default=False)
    emoj = models.CharField(max_length=50)  # 이모지
    emotion1 = models.CharField(max_length=100, blank=True, null=True)
    emotion2 = models.CharField(max_length=100, blank=True, null=True)
    emotion3 = models.CharField(max_length=100, blank=True, null=True)
    content1 = models.TextField()  # 본문 1
    content2 = models.TextField()  # 본문 2
    content3 = models.TextField()  # 본문 3