from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    path('list/', views.article_list, name='article_list'),
    path('detail/<int:id>/', views.article_detail, name='article_detail'),
    path('create/', views.article_create, name='article_create'),
    path('delete/<int:id>', views.article_delete, name='article_delete'),
    path('safe_delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('update/<int:id>/', views.article_update, name='article_update'),

]
