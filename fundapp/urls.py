from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name='home'),
    path('campaign/', views.campaign,name='causes'),
    path('about/', views.about,name='abouts'),
    path('login/', views.handleLogin,name='login'),
    path('signup/', views.handleSignup,name='signup'),
    path('logout/', views.handleLogout,name='logout'),
    path('contact/', views.contact,name='contact'),
    path('startfund/', views.startfund,name='startfund'),
    path('campaign/campaigndetails/', views.campaigndetails,name='campaindetails'),
    path('campaignstatus/', views.campaignstatus,name='campainstatus'),
    path('campaignstatus/fundclaiming/', views.fundclaiming,name='claim-fund'),
    # path('<str:hawa>/',views.hawa,name='404'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)