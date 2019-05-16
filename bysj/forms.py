from django import forms
from bysj import models
from django.core.exceptions import ValidationError
import hashlib

# BootstropForm
class BSForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义操作
        for field in self.fields.values():
            if not isinstance(field, forms.BooleanField):
                # field.widget.attrs['class'] = 'form-control'
                field.widget.attrs.update({'class': 'form-control'})

# 注册的form
class RegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='密码', min_length=6)  # 重写默认字段
    re_password = forms.CharField(widget=forms.PasswordInput, label='确认密码', min_length=6)  # 新增字段

    class Meta:
        model = models.UserInfo  # 指定model
        fields = '__all__'  # ['username','password']  # 指定字段
        exclude = ['is_active']

        labels = {
            'username': '用户名'
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'})

        }
        error_messages = {
            'min_length': '不能少于6位'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义操作
        for field in self.fields.values():
            # field.widget.attrs['class'] = 'form-control'
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        pwd = self.cleaned_data.get('password', '')
        re_pwd = self.cleaned_data.get('re_password', '')
        # print('>>>>>>>>>>>>',pwd, re_pwd)
        if pwd == re_pwd:
            # 密码加密
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            pwd = md5.hexdigest()
            # print(pwd)

            self.cleaned_data['password'] = pwd
            return self.cleaned_data
        # 两次密码不一致
        self.add_error('re_password', '两次密码不一致!!')

        raise ValidationError('两次密码不一致')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        exclude = ['password', 'roles', 'is_active']



