from django.contrib import admin
from .models import ArticlePost
from .models import ArticleColumn

# 后台管理AticlePost数据库
admin.site.register(ArticlePost)

# 注册文章栏目
admin.site.register(ArticleColumn)
