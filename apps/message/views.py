# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 常规模块的引入分为三部分，依次为：
# Python内置模块（如json、datetime）、第三方模块（如Django）、自己写的模块
import json

from django.shortcuts import render, HttpResponse  # render方法实现后台页面渲染，HttpResponse方法实现后端通过HTTP协议同前端通信
from django.views.generic import View  # 使用Django的view视图类
from django.contrib.auth.decorators import login_required  # 登录验证
from django.utils.decorators import method_decorator  # 装饰视图类函数
from django.core.paginator import Paginator  # 分页器
from django.urls import reverse  # url的反转
from django.http import HttpResponseRedirect

from message.models import *
from message.forms import *
from user.models import *


class IndexView(View):
    """首页"""

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def get(self, request):
        user = request.user.username
        allmessages = Articles.objects.all()
        return render(request, 'list.html', {'allmessages': allmessages, 'username': user}) # 返回所有留言页面


class AddMessage(View):
    """增加、修改留言"""

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def get(self, request):
        user = request.user.username
        return render(request, 'add.html', {'username': user})

    def post(self, request):
        articles_form = ArticlesForm(request.POST) 
        if articles_form.is_valid():
            # 获取前端form表单传过来的数据
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')
            id = request.GET.get('pk', '')  # 如果有id，说明不是新增留言，是修改留言
            author = request.user.username  # 获取作者
        else:
            return HttpResponse(json.dumps({'status': 'failed', 'msg': '标题不能为空！'}),
                                content_type='application/json')

        # 判断留言是否为空
        if not content:
            return HttpResponse(json.dumps({"status": "fail"}), content_type='application/json')

        # 修改留言
        if id:
            try:
                articles = Articles.objects.get(id=id)
                articles.title = title
                articles.content = content
                articles.save()
                return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
            except BaseException as e:
                return HttpResponse(json.dumps({"status": "fail"}), content_type='application/json')

        # 新增留言
        else:
            try:
                articles = Articles()
                articles.title = title
                articles.author = UserInfo.objects.get(username=author)
                articles.create_time = datetime.now()
                articles.content = content
                articles.save()
                return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
            except BaseException as e:
                return HttpResponse(json.dumps({"status": "fail", "msg": "新增留言失败，请重新输入"}),
                                    content_type='application/json')


class AllMessages(View):
    """所有留言列表"""

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def get(self, request):
        # 返回所有留言的列表
        allmessages = Articles.objects.all().order_by('-create_time')

        # 分页
        paginator = Paginator(allmessages, 10)  # 每页显示10个对象
        page = request.GET.get('page', '')
        try:
            allmessages = paginator.page(page)
        except BaseException as e:
            allmessages = paginator.page(1)  # 出现任何异常，均显示第一页

        return render(request, 'list.html', {'allmessages': allmessages})


class MyMessages(View):
    """我的留言列表"""

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def get(self, request):
        # 返回留言列表页
        user = request.user.username
        author = UserInfo.objects.get(username=user).id
        allmessages = Articles.objects.filter(author=author).order_by('-create_time')

        # 分页
        paginator = Paginator(allmessages, 10)  # 每页显示10个对象
        page = request.GET.get('page', '')
        try:
            allmessages = paginator.page(page)
        except BaseException as e:
            allmessages = paginator.page(1)  # 出现任何异常，均显示第一页

        return render(request, 'list.html', {'allmessages': allmessages})


class MessageDetail(View):
    """留言详情"""

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def get(self, request):
        # 返回留言详情信息
        message_id = request.GET.get('pk', '')
        try:
            message = Articles.objects.get(id=message_id)  # 获取留言
            message.click_nums += 1
            message.save()  # 点击数+1

            comments = Comment.objects.filter(article_id=message_id).order_by('-add_time')  # 获取评论评论

            # 分页
            paginator = Paginator(comments, 20)  # 每页显示20个对象
            page = request.GET.get('page', '')
            try:
                comments = paginator.page(page)
            except BaseException as e:
                comments = paginator.page(1)  # 出现任何异常，均显示第一页

            context = {
                'message': message,
                'comments': comments,
            }
            return render(request, 'detail.html', context)
        except BaseException as e:
            return render(request, 'detail.html', {})


class MessageDel(View):
    """删除留言"""

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def get(self, request):
        # 处理留言删除操作
        message_id = request.GET.get('pk', '')
        try:
            user = request.user.username
            message = Articles.objects.get(pk=message_id)
            author = UserInfo.objects.get(username=user).id
            # 判断当前用户是否为留言作者
            if message.author_id != author:
                # 返回留言详情页
                return HttpResponseRedirect('/detail/?pk=' + message_id)
            else:
                # 执行删除操作
                message.delete()
                return HttpResponseRedirect(reverse("allmessages"))
        except BaseException as e:
            return HttpResponseRedirect('/detail/?pk=' + message_id)


class CommentView(View):
    """评论"""

    def post(self, request):
        add_form = CommentForm(request.POST)  # 验证评论内容
        try:
            if add_form.is_valid():
                content = request.POST.get("content", "")
                message_id = request.POST.get("message_id", "")
                comment = Comment(user=request.user, content=content, article_id=message_id)
                comment.save()  # 增加评论数据
                message = Articles.objects.get(id=message_id)
                new_nums = Comment.objects.filter(article_id=message_id).count()
                message.comment_nums = new_nums
                message.save()  # 更新评论数

                return HttpResponse(
                    json.dumps({'status': 'success', 'msg': '评论提交成功！', 'comment_nums': new_nums}),
                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'failed', 'msg': '评论失败，请重新评论！'}),
                                    content_type='application/json')
        except BaseException as e:
            print(e)
            return HttpResponse(json.dumps({'status': 'failed', 'msg': '评论失败，请重新评论！'}),
                                content_type='application/json')
