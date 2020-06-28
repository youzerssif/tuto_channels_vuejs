from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'channel_app'
urlpatterns = [
    path('', views.home, name='home'),
    # path('chatapp/', views.chat, name='chat'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('login/', views.loginpage, name='login'),
    path('connect', views.connexion, name='connect'),
    path('deconnexion', views.deconnexion, name='deconnexion'),

]