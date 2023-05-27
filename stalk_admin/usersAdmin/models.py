from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 用户信息表
class UserInfo(models.Model):
    gender = models.CharField(max_length=10, default='未设置', blank=True, null=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.user.username
