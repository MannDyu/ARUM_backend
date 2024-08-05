from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hospital(models.Model):
    hp_name = models.CharField(max_length=50)
    hp_address = models.CharField(max_length=100)
    hp_phone = models.CharField(max_length=15,null=True)

class Self_test(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  #유저와의 연결
    test_score = models.IntegerField()
    test_date = models.DateField(auto_now=True) #레코드가 생성되거나 업데이트될 때마다 날짜를 자동으로 설정

class Self_test_result(models.Model):
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    result_subheading = models.CharField(max_length=30)
    result_content = models.CharField(max_length=80)
    result_image = models.ImageField(upload_to='images/server',blank=True,null=True) 

class Search_center(models.Model):
    city = models.CharField(max_length=5)
    district = models.CharField(max_length=10)