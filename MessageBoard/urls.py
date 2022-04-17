"""messageboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('message/', include('message.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve


from message.views import *
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),  # 首页
    path('register/', RegisterView.as_view(), name='register'),  # 注册
    path('login/', LoginView.as_view(), name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),   
    path('addmessage/', AddMessage.as_view(), name='addmessage'),  
    path('allmessages/', AllMessages.as_view(), name='allmessages'),  
    path('mymessages/', MyMessages.as_view(), name='mymessages'),  
    path('detail/', MessageDetail.as_view(), name='detail'),  
    path('delmessage/', MessageDel.as_view(), name='delmessage'),  
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # 富文本编辑器
]

if settings.DEBUG:
    #  配置静态文件访问问题的处理
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
    urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}))
