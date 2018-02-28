import re

from django import forms

from operation.models import UserAsk


# ModelForm可以直接save
class UserAskFrom(forms.ModelForm):
    # 此处可添加自己的字段
    class Meta:
        model = UserAsk # 选择表单对应的model
        fields = ['name', 'mobile', 'course'] # 选择需要的表单字段

    # 重写clean_field函数可以自定义校验规则，django会自动调用
    def clean_mobile(self):
        reg = '^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$'
        f = re.compile(reg)
        # self.cleaned_data['***'] 可以获取表单数据
        mobile = self.cleaned_data['mobile']
        if f.match(mobile):
            return mobile
        else:
            # 抛出错误
            raise forms.ValidationError('手机号码错误', code='mobile_invalid')