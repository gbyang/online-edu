from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField('昵称', max_length=12, default='')
    birthday = models.DateField('生日', blank=True, null=True)
    gender = models.CharField('性别',max_length=6, choices=(('male', '男'), ('female', '女')), default='male')
    address = models.CharField('地址', max_length=50, default='')
    mobile = models.CharField('手机', max_length=11, default='')
    image = models.ImageField('头像',upload_to='media/img', default='img/batman.png',blank=True,null=True, max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_unread_nums(self):
        # 获取未读消息的数量
        from operation.models import UserMessage  # 不能放上面，不然会造成循环引用
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyCode(models.Model):
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField('验证码类型',choices=(('register', '注册'), ('forget', '找回密码'), ('update_em', '修改邮箱')), max_length=10)
    send_time = models.DateTimeField('发送时间',default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}({})".format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='media/banner')
    url = models.URLField('访问地址', max_length=50)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间',default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name