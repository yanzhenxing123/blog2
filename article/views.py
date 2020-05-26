from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def article_list(request):
    articles = ArticlePost.objects.all()
    context = {
        'articles':articles
    }
    return render(request, 'article/list.html', context=context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])
    context = {
        'article': article
    }
    return render(request, 'article/detail.html', context=context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect(reverse('article:article_list'))
        else:
            return HttpResponse('表单内容填写有误')
    else:
        # article_post_form = ArticlePostForm()
        # context = {
        #     'article': article_post_form
        # }a
        return render(request, 'article/create.html')

@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    user = User.objects.get(articlepost__id=id)
    if request.user != user:
        return HttpResponse('你没有权限删除此文章')
    else:
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect(reverse('article:article_list'))


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    user = User.objects.get(articlepost__id=id)
    # 等价于
    # user = User.objects.filter(articlepost__id=id)
    if request.user != user:
        return HttpResponse('你没有权限删除此文章')
    else:
        if request.method == 'POST':
            article = ArticlePost.objects.get(id=id)
            article.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("仅允许post请求")

@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    user = User.objects.filter(articlepost__id=id).first()
    print(user)
    if request.user != user:
        return HttpResponse('你没有权限修改此文章')
    else:
        if request.method == 'POST':
            article_post_form = ArticlePostForm(request.POST)
            if article_post_form.is_valid():
                title = article_post_form.cleaned_data.get('title')
                body = article_post_form.cleaned_data.get('body')
                ArticlePost.objects.filter(id=id).update(title=title, body=body)

                return redirect("article:article_detail", id=id)
            else:
                return HttpResponse("表单内容有误，请重新填写")
        else:
            article = ArticlePost.objects.get(id=id)
            # 创建表单类实例
            article_post_form = ArticlePostForm()
            # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
            context = {'article': article, 'article_post_form': article_post_form}
            # 将响应返回到模板中
            return render(request, 'article/update.html', context)