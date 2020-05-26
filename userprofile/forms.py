
from django import forms
from django.contrib.auth.models import User
from .models import Profile

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegiseterForm(forms.ModelForm):
    password = forms.CharField()
    password_repeat = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super(UserRegiseterForm, self).clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError('两次密码输入不一致')
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'bio']





