from django.urls import path

from . import views

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete/<int:id>/', views.user_delete, name='delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('edit/<int:id>/', views.profile_edit, name='edit')
]