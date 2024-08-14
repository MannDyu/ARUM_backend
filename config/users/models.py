from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#RefreshToken
class RefreshTokenModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh_token = models.TextField()  #Token 문자열 저장
    created_at = models.DateTimeField(auto_now_add=True)  #생성일자
    expires_at = models.DateTimeField()  #만료일자

    def __str__(self):
        return f"RefreshToken for {self.user.username}"

#Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=50)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
