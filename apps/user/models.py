from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfo(AbstractUser):
    """用户管理"""
    info = models.TextField(verbose_name="个人简介", default='', blank=True, null=True)
    image = models.ImageField(upload_to='images/users', default='images/users/default.png', max_length=100)

    class Meta:  # 元类，可定义该模块的基本信息
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name

    def __str__(self):  # 当print输出实例对象，或str() 实例对象时，调用这个方法
        return self.username
