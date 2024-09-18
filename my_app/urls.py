"""
URL configuration for my_app project.

"""
from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', index_page, name='index'),
    path('home/', index_page, name='home'),
    
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    
    path('order/<int:recipe_id>/', order_page, name='order'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    path('profile/', profile_page, name='profile'),
]
