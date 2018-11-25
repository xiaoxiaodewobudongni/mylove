from django.conf.urls import url

from user.views import *

urlpatterns =[
    url(r'^login/$',LoginView.as_view(),name="login"),   #登录
    url(r'^reg/$',RegisterView.as_view(),name="reg") ,  #注册
    url(r'^forget/$',ForgetPassView.as_view(),name="forget") , #忘记密码
    url(r'^member/$',MenmerView.as_view(),name="member"),  #个人中心
    url(r'^own/$',OwnView.as_view(),name="own"),  #个人资料
    url(r'^up_own/$',UploadImageView.as_view(),name="own_up"),  #修改个人资料
    url(r'^upload_head/$',UploadImageView.as_view(),name="upload_head"), #修改头像
    url(r'^sendmess/$',send_message,name="sendMsg")  #发送短信地址
]
