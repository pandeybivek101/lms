from django.urls import path, re_path
from .views import *
from chat import views


urlpatterns = [
   path('chat/', views.Chat, name='chat'),
   path('chat/<str:room_name>/', views.Room, name='room'),
]
