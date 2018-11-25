from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from db.base_model import BaseModel

"""
Id 主键
	Create_time 创建时间	datetime（用户注册的时间）
	Update_time 更新时间 datetime  （用户修改信息的时间）
	Is_delete 是否删除  boolean		（假删除）
	Nickname 用户名	varchar
	Telephone 手机号	varchar	
	Password	密码	varchar 	(哈希加密)
	Gender		性别	choice		(男， 女， 保密)
	Birthday	生日	datetime
	School		学校	varchar
	Location	地址	varchar
	Hometown	地址	varchar
	"""

class UserInfo(BaseModel):
    """用户表"""
    gender = (
        ("男",1),
        ("女",2),
              )
    nickname = models.CharField(max_length=50,verbose_name="用户名")
    telephone = models.CharField(max_length=11,verbose_name="电话号码",
    validators = [
        RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
    ]
    )
    password = models.CharField(max_length=32,verbose_name="密码")
    gender = models.SmallIntegerField(choices=gender,default=1,verbose_name="性别")
    birthday = models.DateField(null=True,blank=True,verbose_name="生日")
    school = models.CharField(max_length=50,null=True,blank=True,verbose_name="学校")
    location = models.CharField(max_length=50,null=True,blank=True,verbose_name="地址")
    hometown = models.CharField(max_length=50,null=True,blank=True,verbose_name="家乡")
    head = models.ImageField(max_length=200,upload_to='img/%Y/%m/%d',
                             default='images/default.jpg',verbose_name='头像')

    def __str__(self):
        return self.telephone

    class Meta:
        db_table = "user"
        verbose_name = "用户管理"
        verbose_name_plural = "用户管理"


