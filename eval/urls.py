from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/<int:pk>', views.eval_home, name='eval_home'),
    path('more_jobs/<int:pk>', views.more_jobs, name='more_jobs'),
    path('current_job/<int:pk>', views.current_job, name='current_job'),
    path('select_product/<int:pk>,<int:prod>', views.select_eval_product, name='select_eval_product'),
    path('complete_eval/<int:pk>,<int:prod>', views.complete_eval_product, name='complete_eval_product'),
    path('history/<int:pk>', views.evaluation_history, name='evaluation_history'),
    path('login', views.eval_loginForm, name='eval_loginForm'),
    path('signup', views.eval_signup, name='eval_signup'),
    path('logout', views.eval_logout, name='eval_logout'),

    path('update-password/', views.update_password, name='update_password'),
    path('update-phone/', views.update_phone, name='update_phone'),
    path('view-profile/<int:pk>/', views.view_profile, name='view_profile'),

]