import hashlib
import uuid

from django.conf import settings
from django.shortcuts import redirect
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from user.models import UserInfo

#密码加密
def set_password(password):
    """

    :param password: 密码
    :return: 加密后的密码
    """
    new_password = "{}{}".format(password,settings.SECRET_KEY)
    h  = hashlib.md5(new_password.encode("utf-8"))
    return h.hexdigest()

#得到session
def get_session(request,user):
    """

    :param request: request对象
    :param user: 用户名
    :return: session状态
    """
    request.session['ID'] = user.pk
    request.session['telephone'] = user.telephone
    request.session['head'] = user.head

#定义session
def verify_login_required(func):
    """
    :param func:传入的函数
    :return:登录验证session
    """
    def verify(request,*args,**kwargs):
        #判断session中是否有ID,如果没有说明没有登录,请登录
        if request.session.get("ID")is None:
            #配置文件中获取当前的url地址
            login_url= settings.LOGIN_URL
            return redirect(login_url)
        else:  #返回被调用的函数
            return func(request,*args,**kwargs)
    return verify


REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


if __name__ == '__main__':
    __business_id = uuid.uuid1()
    # print(__business_id)
    params = "{\"code\":\"12345\",\"product\":\"云通信\"}"
    # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    print(send_sms(__business_id, "13000000000", "云通信测试", "SMS_5250008", params))

