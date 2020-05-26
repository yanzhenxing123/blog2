from django.shortcuts import render, redirect, reverse
from .forms import UserLoginForm, UserRegiseterForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Profile

def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            password = user_login_form.cleaned_data.get('password')
            username = user_login_form.cleaned_data.get('username')
            # authenticate()方法验证用户名称和密码是否匹配，如果是，则将这个用户数据返回。
            user = authenticate(username=username, password=password)
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect(reverse('article:article_list'))
            else:
                return HttpResponse("您的账号或密码有误")
        else:
            return HttpResponse('账号或者密码不合法')
    elif request.method == "GET":
        user_login_form = UserLoginForm()
        context = {
            'form':user_login_form
        }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请使用GET或POST请求')

@require_http_methods(["POST", "GET"])
def user_logout(request):
    logout(request)
    return redirect(reverse('article:article_list'))

class RegisterView(View):
    def get(self, request):
        return render(request, 'userprofile/register.html')

    def post(self, requset):
        user_register_form = UserRegiseterForm(requset.POST)
        if user_register_form.is_valid():
            password = user_register_form.cleaned_data.get('password')
            email = user_register_form.cleaned_data.get('email')
            username = user_register_form.cleaned_data.get('username')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('userprofile:login'))
        else:
            return HttpResponse('您的表单输入有误，请重新输入')

# 装饰器 给视图函数添加功能
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            return redirect(reverse('article:article_list'))
        else:
            return HttpResponse('你没有操作的权限')
    else:
        return HttpResponse('必须是POST请求')


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)

    if request.method == "POST":
        if request.user != user:
            # 如果修改数据的人不是本人
            return HttpResponse('你没有此权限修改此内容')
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            if not Profile.objects.filter(user_id=id).exists():
                profile = Profile.objects.create(user=user)
            else:
                profile = Profile.objects.get(user_id=id)
            profile.phone = profile_form.cleaned_data.get('phone')
            profile.bio = profile_form.cleaned_data.get('bio')

            if 'avatar' in request.FILES:
                profile.avatar = profile_form.cleaned_data.get('avatar')
            profile.save()

            # 两种方式等价 下面这一种的操作对象是一个QuerySet，性能较好

            # phone = profile_form.cleaned_data.get('phone')
            # bio = profile_form.cleaned_data.get('bio')
            # if 'avatar' in request.FILES:
            #     avatar = profile_form.cleaned_data.get('avatar')
            # else:
            #     avatar = ''
            # Profile.objects.filter(user_id=id).update(phone=phone, bio=bio)

            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse('您的表单输入有误， 请重新输入')


    elif request.method == 'GET':
        if Profile.objects.filter(user_id=id).exists():
            profile = Profile.objects.get(user_id=id)
        else:
            profile = Profile.objects.create(user=user)
        profile_form = ProfileForm()
        context = {
            'profile_form':profile_form,
            'profile': profile,
            'user': user
        }
        return render(request, 'userprofile/edit.html', context=context)
    else:
        return HttpResponse('请使用GET或POST请求')
