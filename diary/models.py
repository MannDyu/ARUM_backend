from django.db import models
from django.contrib.auth.models import User

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    emoj = models.CharField(max_length=20)
    emotion1 = models.CharField(max_length=100, blank=True, null=True)
    emotion2 = models.CharField(max_length=100, blank=True, null=True)
    emotion3 = models.CharField(max_length=100, blank=True, null=True)
    content1 = models.TextField()
    content2 = models.TextField()
    content3 = models.TextField()