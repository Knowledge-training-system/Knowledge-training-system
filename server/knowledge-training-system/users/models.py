from django.db import models
from django.contrib.auth.models import User 
#from django.contrib.auth.models import AbstractUser, BaseUserManager  

from django.dispatch import receiver
from django.db.models.signals import post_save


class ExtraUser(models.Model):  # 一对一方式扩展
    theUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name="extra")  # 注意这里更改User中自添加的extrauser字段改名为extra
    gender = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    identity = models.CharField(max_length=20, null=True)
    phonenum = models.CharField(max_length=20, null=True)
    
    class Meta:
        db_table = 'ExtraUser'

@receiver(post_save, sender=User)  # 当User产生post_save信号时 
def handler_user_extra_content(sender, instance, created, **kwargs):
    if created:  # 如果第一次创建
        ExtraUser.objects.create(theUser=instance)  # 绑定User实例到ExtraUser的all_user字段
    instance.extra.save()  # 保存ExtraUser的内容 ,注意extra是ExtraUser的all_user字段外键的related_name名




"""
class UserManager(BaseUserManager):  
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError("必须传递用户名")
        if not password:
            raise ValueError("必须传递密码")
        user = self.model(phone=phone, username=username, **kwargs)  # self.model表示当前模型
        user.set_password(password)  # password只能这样设置
        user.save()
        return user

    def create_user(self, phone, username, password, **kwargs):
        kwargs["is_superuser"] = False  # 添加is_superuser键值对
        return self._create_user(phone=phone, username=username, password=password, **kwargs)

    def create_superuser(self, phone, username, password, **kwargs):
        kwargs["is_superuser"] = True
        return self._create_user(phone=phone, username=username, password=password, **kwargs)
"""

"""
class User(AbstractUser):  # 自定义的User类
    REQUIRED_FIELDS = []  # 命令行创建超级用户的时候系统提示要添加的内容

    username = models.CharField(max_length=20,primary_key = True) #第一位为0是学生 旧：userId
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=5, null=True)
    age = models.IntegerField(null=True)
    identity = models.CharField(max_length=20, null=True)
    phonenum =models.CharField(max_length=20, null=True)
    email = models.EmailField( null=True)
    first_name = models.CharField( max_length=30, blank=True, null=True)
    last_name = models.CharField( max_length=150, blank=True, null=True)
    is_staff = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    #email = models.EmailField( blank=True)
    #last_login = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default = False)

    class Meta:
        db_table = 'users'
"""


"""
INSERT INTO `ktsdb`.`users` (`username`, `password`) VALUES ('000011', '1');
INSERT INTO `ktsdb`.`users` (`username`, `password`) VALUES ('000004', '1');
INSERT INTO `ktsdb`.`users` (`username`, `password`) VALUES ('000005', '1');
INSERT INTO `ktsdb`.`users` (`username`, `password`) VALUES ('100004', '1');





有趣函数
@receiver(post_save,sender=USER)
def create_user_extension(sender,instance,created,**kwargs):
    if created:
        UserExtension.objects.create(USER=instance)
    else:
        instance.extension.save()
"""


"""
class User(models.Model):
    userId = models.CharField(max_length=20,primary_key = True) #第一位为0是学生
    password = models.IntegerField()
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=5)
    age = models.IntegerField()
    identity = models.CharField(max_length=20)
    phonenum =models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        db_table = 'users'
"""