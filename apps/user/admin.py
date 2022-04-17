from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # 处理后台管理用户时，密码加密问题

from user.models import *


@admin.register(UserInfo)
class UserInfoAdmin(UserAdmin):
    list_display = ['username']  # 定义该model下内容列表中，展示的属性
    list_filter = ['username']  # 定义可筛选的属性
    search_fields = ['username']  # 定义可搜索的属性
    fieldsets = (
        ('用户信息', {
            'fields': ('username', 'password', 'image', 'info')
        }),
    )
