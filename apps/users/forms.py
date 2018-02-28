from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

# 使用类来处理表格
class LoginForm(forms.Form):
    # 定义form中各字段需要满足的要求
    # 变量名必须与form中input的name属性值一致
    username = forms.CharField(required=True, min_length=6)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={'invalid':"验证码错误"}) # 添加验证码


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':"验证码错误"}) # 添加验证码


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


# 利用ModelForm来保存图片对象
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','gender','address','mobile']