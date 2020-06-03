from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class ArticleColumn(models.Model):
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    # 文章作者，为外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()

    # created time
    created = models.DateTimeField(default=timezone.now)

    # 修改时间
    updated = models.DateTimeField(auto_now=True)

    # 浏览量
    total_views = models.PositiveIntegerField(default=0)  # 储存正整数的字段，初始值为零

    # 文章栏目的“一对多”外键
    '''
    null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空，那么在新建一个model对象的时候是不会报错的！！
    blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填
    '''
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article')

    class Meta:
        db_table = 'article_post'
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])








