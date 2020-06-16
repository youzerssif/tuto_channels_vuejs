from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'channel_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('chatapp/', views.chat, name='chat'),

]