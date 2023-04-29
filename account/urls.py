from django.urls import path

from . import views

urlpatterns = [
    path('', views.account, name='account_home'),
    path('register', views.register, name='register'),
    path('login', views.login_acc, name='login'),
    path('logout', views.logout_acc, name='logout'),
]
