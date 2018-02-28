from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyCode
from MxOnline.settings import EMAIL_FROM

def create_random_str(length=8):
    str = ''
    char = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    random = Random()
    char_len = len(char)-1
    for i in range(0, length):
        str += char[random.randint(0, char_len)]
    return str


def send_register_email(email, send_type='register'):
    evf = EmailVerifyCode()
    if send_type == 'update_em':
        code = create_random_str(4)
    else:
        code = create_random_str(16)
    evf.email = email
    evf.code = code
    evf.send_type = send_type
    evf.save()

    mail_title = ''
    mail_body = ''
    if evf.send_type == 'register':
        mail_title = 'gbyang的网站的注册激活链接'
        mail_body = '请单击以下链接进行激活 http://127.0.0.1:8000/active/{}'.format(code)
        # 发送邮件 需要在setting进行相关配置
        send_status = send_mail(mail_title, mail_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif evf.send_type == 'forget':
        mail_title = 'gbyang的网站的密码重置链接'
        mail_body = '请单击以下链接进行密码重置 http://127.0.0.1:8000/reset/{}'.format(code)
        # 发送邮件 需要在setting进行相关配置
        send_status = send_mail(mail_title, mail_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif evf.send_type == 'update_em':
        mail_title = 'gbyang的网站的邮箱重置链接'
        mail_body = '您的验证码是: {}'.format(code)
        # 发送邮件 需要在setting进行相关配置
        send_status = send_mail(mail_title, mail_body, EMAIL_FROM, [email])
        if send_status:
            pass