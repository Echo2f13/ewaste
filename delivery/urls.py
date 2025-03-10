from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/<int:pk>', views.dlv_home, name='dlv_home'),
    path('signup', views.dlv_signup, name='dlv_signup'),
    path('login', views.dlv_loginForm, name='dlv_loginForm'),
    path('logout', views.dlv_logout, name='dlv_logout'),
]