from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Quest(models.Model):
    qs_theme = models.CharField(max_length=2)
    qs_content = models.CharField(max_length=30)

class Quest_history(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  #유저와의 연결
    qs_theme = models.CharField(max_length=2)
    qs_content = models.CharField(max_length=30)
    qs_date = models.DateField(auto_now_add=True)
    qs_perform_yn = models.BooleanField(default=False)
    qs_perform_content = models.TextField(blank=True)
    qs_perform_image = models.ImageField(upload_to='images/',blank=True,null=True) 
    ##여기서 blank=true옵션만 주면 NULL 값을 허용하지 않기 때문에, 값이 입력되지 않은 경우 빈 문자열 ('')로 저장
    ##ImageField의 경우에는 파일 경로를 저장하기 때문에, 빈 문자열을 사용하는 것이 적절하지 않음 so,null=true옵션 같이 줌