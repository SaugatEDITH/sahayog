from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('campaign/', views.campaign,name='causes'),
    path('about/', views.about,name='abouts'),
    path('login/', views.handleLogin,name='login'),
    path('signup/', views.handleSignup,name='signup'),
    path('logout/', views.handleLogout,name='logout'),
    path('contact/', views.contact,name='contact'),
    # path('<str:hawa>/',views.hawa,name='404'),
]