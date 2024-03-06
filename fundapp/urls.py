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
    path('search/', views.search_campaigns, name='search_campaigns'),
    path('startfund/', views.startfund,name='startfund'),
    path('campaign/<str:slug>/', views.campaigndetails,name='campaindetails'),
    path('campaignstatus/', views.campaignstatus,name='campainstatus'),
    path('campaignstatus/fundclaiming/<int:post_id>', views.fundclaiming,name='claim-fund'),
    path('campaignstatus/editCampaign/<int:post_id>', views.editCampaign,name='editCampaign'),
    # for deleting campaigns
    path('campaignstatus/deleteCampaign/<int:post_id>', views.deleteCampaign, name='deleteCampaign'),
    # for updating campaigns
    path('campaignstatus/updateCampaign/<int:post_id>', views.updateCampaign, name='updateCampaign'),
    
    # for esewa donation
    path("campaign/<str:slug>/esewasahayog/", views.esewasahayog, name="esewasahayog"),
    # for esewa success url
    path("<str:slug>/esewa-payment-success/<int:res>", views.payment_is_successful, name="payment_is_successful_esewa")


    # path('<str:hawa>/',views.hawa,name='404'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)