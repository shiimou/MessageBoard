# !/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # 处理后台管理用户时，密码加密问题

from message.models import *


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_time', 'click_nums']
    list_filter = ['title']
    search_fields = ['title']
    readonly_fields = ['click_nums', 'comment_nums']  # 只读字段


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'user']
    list_filter = ['article', 'user']
    search_fields = ['article', 'user']
