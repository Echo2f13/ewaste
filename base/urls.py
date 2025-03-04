from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('loginForm', views.loginForm, name='loginForm'),
    path('signupForm', views.signupForm, name='signupForm'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('home/<int:pk>', views.home, name='home'),
    path('sell/<int:pk>', views.sell, name='sell'),
    path('product/<int:pk>/<int:pk2>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/<int:pk2>/', views.add_to_cart, name='add_to_cart'),

    path('profile/<int:pk>/', views.profile, name='profile'),
    path('change_address/', views.change_address, name='change_address'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
]