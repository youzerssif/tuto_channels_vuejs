
# chat/routing.py
from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    # path('ws/chat/<slug:room_name>/', consumers.ChatConsumerEditor),
    # path('ws/salon/<slug:room_name>/', consumers.ChatConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    # path('ws/suggest/suggestion/', consumers.ChatSuggestion),
]

    
      
    
            