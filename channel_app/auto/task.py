#------ WS
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def hello():
    
    layer = get_channel_layer()
    data = {
        'mes': 'le cours prend fin dans 10 min',
        'user': 'Admin',# UPDATE QR CODE
        
        
    }
    async_to_sync(layer.group_send)('chat_hello', {
            'type': 'chat_message',
            'message': data,
            
        })