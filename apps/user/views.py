import random
import uuid

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
import re

# Create your views here.
from django.views import View

from db.base_view import BaseVerifyView
from user.helper import set_password, get_session, send_sms
from user.forms import RegisterForm, LoginForm, InfoModelForm, UploadImageModelForm, UploadPassword
from user.models import UserInfo
from django_redis import get_redis_connection


# class LoginView(View):
#     """登录"""
#     def get(self,request):
#         return render(request, "user/login.html")
#
#     def post(self,request):
#         login_form = LoginForm(request.POST)
#         # 处理数据
#         if login_form.is_valid():
#             username = login_form.cleaned_data['telephone']
#             password = login_form.cleaned_data['password']
#             # 获取用户名
#             try:
#                 user = UserInfo.objects.get(telephone=username)
#             except UserInfo.MultipleObjectsReturned:
#                 # 获取多个用户
#                 return redirect("user:login")
#             except UserInfo.DoesNotExist:
#                 # 用户名不存在
#                 return redirect("user:login")
#             # 判断密码是否正确 ,先加密
#             password = set_password(password)
#             if password != user.password:
#                 return redirect("user:login")
#             # 如果正确,登录保存到session中
#             # request.session['ID'] = user.pk
#             # request.session['username'] = user.telephone
#             # 跳转到个人中心
#             return redirect("user:member")
#         else:
#             context = {
#                 "errors": login_form.errors
#             }
#             return render(request, "user/login.html", context)
class LoginView(View):
    """登录"""
    def get(self,request):
        return render(request,"user/login.html")
    def post(self,request):
        login_form = LoginForm(request.POST)  #创建form对象
        if login_form.is_valid():  #合法
            #得到清洗过的用户
            user = login_form.cleaned_data.get("user")
            #保存进session中,跳转到个人中心
            get_session(request,user)
            return redirect("user:own")
        else:
            context={
                "errors":login_form.errors
            }
            return render(request,"user/login.html",context)



class RegisterView(View):
    """注册"""
    def get(self,request):
        return render(request, "user/reg.html")

    def post(self,request):
        data = request.POST
        reg_form = RegisterForm(data)
        if reg_form.is_valid():
            #合法
            data = reg_form.cleaned_data
            #获取密码 加密
            password = data.get("password1")
            password = set_password(password)
            #添加到数据库
            UserInfo.objects.create(telephone=data.get("telephone"),password=password)
            #返回到登录页
            return redirect("user:login")
        else:
            context ={
                "errors":reg_form.errors
            }
            return render(request,"user/reg.html",context)


class ForgetPassView(View):
    """忘记密码"""
    def get(self,request):
        return render(request,"user/forgetpassword.html")
    def post(self,request):
        #获取form对象
        data = request.POST
        for_form = UploadPassword(data)
        if for_form.is_valid():
            data =  for_form.cleaned_data
            #获取密码
            pwd1 =  data.get("password1")
            tel = data.get("telephone")
            #加密
            password = set_password(pwd1)
            #修改密码
            UserInfo.objects.create(telephone=tel,password=password)
            #返回到登录页
            return redirect("user:login")
        else:
            context = {
                "errors": for_form.errors
            }
            return render(request,"user/forgetpassword.html",context)



class MenmerView(BaseVerifyView):
    """个人中心"""
    def get(self,request):
        return render(request,"user/member.html")
    def post(self,request):
        pass


# class OwnView(BaseVerifyView):
#     """个人资料"""
#     def get(self,request):
#         #从session中获取数据
#         telephone = request.session.get("telephone")
#         #从数据库获取数据
#         user = UserInfo.objects.get(telephone=telephone)
#         user.password = None
#         if user.birthday:
#             user.birthday = user.birthday.strftime("%Y-%m-%d")
#         context = {
#             "user": user,
#         }
#         # return render(request,"user/infor.html",context)
#         return HttpResponse("OK")
#
#     def post(self,request):
#         #接收数据
#         data = request.POST
#         #验证数据
#         form = InfoModelForm(data)
#         if form.is_valid():
#             #清洗数据
#             data = form.cleaned_data
#             telephone = request.POST.get("telephone")
#             #更新
#             UserInfo.objects.filter(telephone=telephone).update(**data)
#             return redirect("user:own")
#         else:
#             context = {
#                 "errors":form.errors
#             }
#             return render(request,"user/infor.html",context)

class OwnView(BaseVerifyView):
    """个人资料"""
    def get(self, request):
        # 查询用户的个人信息 进行回显
        # session中保存了用户的id
        user_id = request.session.get("ID")
        # 根据用户id查询用户信息
        user = UserInfo.objects.get(pk=user_id)
        # 渲染到页面
        context = {
            "user":user
        }
        return render(request, 'user/infor.html',context)

    def post(self, request):
        # 获取当前用户对象
        user_id = request.session.get("ID")
        user = UserInfo.objects.get(pk=user_id)
        user.nickname = request.POST.get("nickname")
        user.gender = request.POST.get("gender")
        # 文件字段
        user.head = request.FILES.get("head")
        user.birth_of_date = request.POST.get("birth_of_date")
        user.save()
        # 重写session
        get_session(request, user)

        # 跳转
        return redirect("sp_user:member")

class UploadImageView(BaseVerifyView):
    """用户头像修改"""
    def post(self,request):
        #根据session获得用户
        user_id = request.session.get("id")
        user = UserInfo.objects.get(pk=user_id)
        #得到from对象
        image_form = UploadImageModelForm(request.POST, request.FILES, instance=user)
        #提交图片
        if image_form.is_valid():
            image_form.save()
            return redirect("users:info")
        else:
            return redirect("users:info")

#发送短信
def send_message(request):
    if request.method == "POST":
        # 接收手机号码,生成随机码,保存到redis中,发送短信
        #得到表单手机号
        phone = request.POST.get("phone","")
        #验证手机号码格式正确,正则验证,创建正则验证
        #得到正则对象
        p_re = re.compile("^1[3-9]\d{9}$")
        #匹配传入的手机号
        rs = re.search(p_re,phone)
        if not rs:
            #手机号码格式错误
            return JsonResponse({"error":1,"errormessage":"手机号码格式错误"})
        #生成随机码
        #  _下划线作为一个无用的东西
        random_code = "".join([str(random.randint(0,9))for _ in range(6)])
        #连接redis
        cnn = get_redis_connection("default")
        #操作数据库,保存随机码
        cnn.set(phone,random_code)
        cnn.expire(phone,300)
        #发送短信,引用模板
        print(random_code)
        # __business_id = uuid.uuid1()
        # # print(__business_id)
        # params = "{\"code\":\"%s\",\"product\":\"重在完成\"}"%random_code
        # # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        # send_sms(__business_id, phone, "注册验证", "SMS_2245271", params)
        return JsonResponse({"error": 0})
    else:
        #返回json格式
        return JsonResponse({"error":1,"errormessage":"请求方式错误"})

