from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from user.helper import set_password
from user.models import UserInfo


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="密码", max_length=16,min_length=6,
                                error_messages={
                                    'required':'密码必须填写',
                                    'max_length':'密码不能超过16位',
                                    'min_length': '密码不能低于6位数'
                                })
    password2 = forms.CharField(label="确认密码", error_messages={"required":"请确认密码"})
    # message = forms.CharField(error_messages={"required":"验证码必须填写"})

    class Meta:
        model = UserInfo
        fields = ["telephone",]
        error_messages = {
            "telephone": {
            "required": "手机号码必须填写"
            }
        }

    def clean_telephone(self):
        """
        验证手机号
        :return:
        """
        tel = self.cleaned_data.get("telephone")
        exists = UserInfo.objects.filter(telephone=tel).exists()
        if exists:
            raise forms.ValidationError("手机号码已经存在!")
        return tel

    def clean_password2(self):
        # 获取两次密码,验证
        pwd1 = self.cleaned_data.get("password1")
        pwd2 = self.cleaned_data.get("password2")
        # 比对
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError("输入密码不一致!")
        return pwd1
    #验证验证码
    # def clean_message(self):
    #     tel = self.cleaned_data.get("telephone")
    #     message = self.cleaned_data.get("message")
    #     #连接redis
    #     r = get_redis_connection("default")
    #     if tel:
    #         code = r.get("phone")
    #         code = code.decode("utf-8")
    #         if code is None:
    #             raise ValidationError("验证码已过期")
    #         if message != code:
    #             raise ValidationError("验证码错误")
    #         return message
    #     else:
    #         return message


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ["telephone","password"]
        error_messages = {
            "telephone":{
                "required":"手机号必须填写"
            },
            "password":{
                "required":"密码必须填写"
            }
        }
    def clean(self):
        #清洗数据,增加用户体验
        cleaned_data = super().clean()
        telephone = cleaned_data.get("telephone")
        password = cleaned_data.get("password")
        if all([telephone,password]):  #如果账号密码存在
            try:
                user = UserInfo.objects.get(telephone=telephone)  #得到用户,根据用户找到密码
            except UserInfo.DoesNotExist:
                raise ValidationError({"telephone":"用户不存在"})
            if user.password != set_password(password):
                raise ValidationError({"password":"密码填写错误"})
            #将用户信息保存到clean_data中
            cleaned_data['user'] = user
            return cleaned_data
        return cleaned_data


class UploadImageModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields= ["head"]


class UploadPassword(forms.ModelForm):
    password1 = forms.CharField(label="密码", max_length=16, min_length=6,
                                error_messages={
                                    'required': '密码必须填写',
                                    'max_length': '密码不能超过16位',
                                    'min_length': '密码不能低于6位数'
                                })
    password2 = forms.CharField(label="确认密码", error_messages={"required": "请确认密码"})
    message = forms.CharField(error_messages={"required": "验证码必须填写"})

    class Meta:
        model = UserInfo
        fields = ["telephone"]
        error_messages = {
            "telephone": {
                "required": "手机号码必须填写"
            }
        }
    def clean_telephone(self):
        """
        验证手机号
        :return:
        """
        tel = self.cleaned_data.get("telephone")
        exists = UserInfo.objects.filter(telephone=tel).exists()
        if not exists:
            raise forms.ValidationError("手机号码不存在!")
        return tel

    def clean_password2(self):
        # 获取两次密码,验证
        pwd1 = self.cleaned_data.get("password1")
        pwd2 = self.cleaned_data.get("password2")
        # 比对
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError("输入密码不一致!请重新输入")
        return pwd1


class InfoModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['nickname','head','birthday']







