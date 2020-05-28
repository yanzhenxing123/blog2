from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        # 排序问题
        if order == 'total_views':
            # 返回QuerySet对象
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()


    # 分页，每页显示一篇文章, 每三个做一页
    paginator = Paginator(article_list, 3)
    # 从GET请求种获取页码数
    page = request.GET.get('page')
    # 获取请求中页码的文章
    articles = paginator.get_page(page)

    context = {
        'articles':articles,
        'order': order,
        'search':search
    }
    return render(request, 'article/list.html', context=context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])  # 只执行total_views优化效率

    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
        ]
    )

    article.body = md.convert(article.body)
    context = {
        'article': article,
        'toc': md.toc,
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

