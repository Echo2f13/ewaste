from django.urls import path
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/<int:pk>', views.dlv_home, name='dlv_home'),
    path('signup', views.dlv_signup, name='dlv_signup'),
    path('login', views.dlv_loginForm, name='dlv_loginForm'),
    path('logout', views.dlv_logout, name='dlv_logout'),
    path('delivery_more_jobs/<int:pk>/', views.delivery_more_jobs, name='delivery_more_jobs'),
    path('delivery_update_password/', views.delivery_update_password, name='delivery_update_password'),
    path('delivery_update_phone/', views.delivery_update_phone, name='delivery_update_phone'),

]