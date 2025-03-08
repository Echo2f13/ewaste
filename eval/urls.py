from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/<int:pk>', views.eval_home, name='eval_home'),
    path('login', views.eval_loginForm, name='eval_loginForm'),
    path('signup', views.eval_signup, name='eval_signup'),
    path('logout', views.eval_logout, name='eval_logout'),

]