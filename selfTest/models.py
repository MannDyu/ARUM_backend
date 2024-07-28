from django.db import models

# Create your models here.
class Hospital(models.Model):
    hp_name = models.CharField(max_length=50)
    hp_address = models.CharField(max_length=100)
    hp_phone = models.CharField(max_length=15,null=True)