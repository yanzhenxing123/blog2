from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment

@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data.get('body')
            user = request.user
            Comment.objects.create(user=user, body=body, article=article)
            return redirect(article)
        else:
            return HttpResponse('您的表单输入有误')
    else:
        return HttpResponse('发表评论仅接受POST请求')







