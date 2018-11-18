from django.conf.urls import url

from todo.views import login

urlpatterns =[
    url(r'^$',login,name="login")
]
