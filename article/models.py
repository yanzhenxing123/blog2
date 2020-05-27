from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

    class Meta:
        db_table = 'article_post'
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created', )

    def __str__(self):
        return self.title




