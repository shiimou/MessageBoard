# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 常规模块的引入分为三部分，依次为：
# Python内置模块（如json、datetime）、第三方模块（如Django）、自己写的模块

from datetime import datetime

from django.db import models  
from ckeditor_uploader.fields import RichTextUploadingField  # 富文本编辑器

from user.models import *


class Articles(models.Model):
    """留言管理"""
    title = models.CharField(verbose_name='标题', max_length=50)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, verbose_name='作者')
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now)
    info = models.CharField(verbose_name='摘要', default='', max_length=100)
    content = RichTextUploadingField('留言内容', config_name='default')  # 富文本编辑器
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    comment_nums = models.IntegerField(verbose_name='评论数', default=0)

    class Meta:  # 元类，可定义该模块的基本信息
        verbose_name = "留言管理"
        verbose_name_plural = verbose_name

    def __str__(self):  # 当print输出实例对象，或str() 实例对象时，调用这个方法
        return self.title


class Comment(models.Model):
    """用户评论"""
    content = models.TextField(verbose_name="评论详情", default='', max_length=500)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='留言')
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='评论用户')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.article)

