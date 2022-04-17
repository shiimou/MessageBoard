import json

from django.shortcuts import render, HttpResponse  # render方法实现后台页面渲染，HttpResponse方法实现后端通过HTTP协议同前端通信
from django.views.generic import View  # 使用Django的view视图类
from django.contrib.auth.hashers import make_password  # django的加密方法
from django.contrib.auth import login, authenticate, logout  # django的用户管理模块
from django.contrib.auth.decorators import login_required  # 登录验证
from django.utils.decorators import method_decorator  # 装饰视图类函数


from user.models import *
from user.forms import *

# Create your views here.
class RegisterView(View):
    """注册"""

    def get(self, request):
        # 返回注册页面
        return render(request, 'register.html', {})

    def post(self, request):
        # 接收注册信息
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password_ = request.POST.get('password_', '')

        # 判断用户名、密码均不为空
        if not username or not password or not password_:
            return HttpResponse(json.dumps({"status": "fail", "msg": "注册信息均不可为空，请重新输入"}),
                                content_type='application/json')
        # 判断两次输入的密码是否一致
        if password_ != password:
            return HttpResponse(json.dumps({"status": "fail", "msg": "两次密码不一致，请重新输入"}),
                                content_type='application/json')
        # 判断该用户是否已注册
        if UserInfo.objects.filter(username=username):
            return HttpResponse(json.dumps({"status": "fail", "msg": "该用户已注册，请重新输入"}),
                                content_type='application/json')
        # 将新注册的用户保存至数据库中
        try:
            user_profile = UserInfo()
            user_profile.username = username
            user_profile.password = make_password(password)  # 对密码进行加密处理
            user_profile.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        except BaseException as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "用户注册失败，请重新输入"}), content_type='application/json')


class LoginView(View):
    """登录"""

    def get(self, request):
        # 返回登录页面
        return render(request, 'login.html', {})

    def post(self, request):
        # 获取用户填写的登录信息
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 判断用户名、密码均不为空
        if not username or not password:
            return HttpResponse(json.dumps({"status": "fail", "msg": "登录信息均不可为空，请重新输入"}),
                                content_type='application/json')
        # 判断用户是否已注册
        if not UserInfo.objects.filter(username=username):
            return HttpResponse(json.dumps({"status": "fail", "msg": "该用户未注册，请注册或重新输入"}),
                                content_type='application/json')
        try:
            # 验证用户登录密码是否匹配
            user = authenticate(username=username, password=password)
            if user:
                # 用户登录
                login(request, user)
                return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "用户名或密码错误，请重新输入"}),
                                    content_type='application/json')
        except BaseException as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "登录失败，请重新输入"}), content_type='application/json')


class LogoutView(View):
    """注销登录操作"""

    def get(self, request):
        try:
            # 注册登录操作
            logout(request)
            return render(request, 'login.html', {})
        except BaseException as e:
            return render(request, 'login.html', {})


class UserInfoView(View):
    """个人中心"""

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def get(self, request):
        return render(request, 'userinfo.html', {})

    @method_decorator(login_required(login_url='/login/'))  # 验证用户是否登录，如未登录转向login路由
    def post(self, request):
        user_img = request.FILES.get('face', '')
        username = request.POST.get('username', '')
        user_info_form = UserInfoForm(request.POST, request.FILES, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()  # 通过验证的内容，可以直接保存
            # 获取头像文件
            if user_img:
                try:
                    # 图片需要单独处理存储，django可自动保存文件，并且如文件首次使用，文件名与上传的名称一致，如有和之前文件重名的，会自动添加随机字符串
                    user = UserInfo.objects.get(username=username)
                    user.image = user_img
                    user.save()
                except BaseException as e:
                    print(e)
            return HttpResponse(json.dumps({'status': 'success', 'msg': '个人信息修改成功！'}), content_type='application/json')
        else:
            # 通过json的dumps方法把字典转换为json字符串
            return HttpResponse(json.dumps({'status': 'failed', 'msg': '个人信息修改失败，请重新修改！'}),
                                content_type='application/json')
