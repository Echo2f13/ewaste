from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('loginForm', views.loginForm, name='loginForm'),
    path('signupForm', views.signupForm, name='signupForm'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]