from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
import json
# from channels.db import database_sync_to_async
from channels.auth import login 
from asgiref.sync import async_to_sync


from .models import Chat
from django.contrib.auth.models import User


# class ChatConsumerEditor(AsyncWebsocketConsumer):
#     async def connect(self):
       
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         # self.room_name = "hello"
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
        

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message'] 
#         print(message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )
     
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
        


#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
            
#             'message': message ,
            
#         }))

# class ChatConsumer(AsyncWebsocketConsumer):
    
    

    
#     async def connect(self):
        
#         # self.username = await database_sync_to_async(self.get_name)()
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         # self.room_name = "hello"
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()
        
#     # def get_name(self):
#     #     return User.objects.all()[0].name

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
        

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message'] 
#         print(message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
        


#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
            
#             'message': message ,
            
#         }))
        
        
        
# chat/consumers.py

class ChatConsumer(WebsocketConsumer):
    
    
    def fetch_messages(self, data):
        print('fetch ')
        messages = Chat.last_10_messages()
        
        
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send(json.dumps(content))
        # print(json.dumps(content))
    
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    
    def message_to_json(self, message):
        return {
            'author':message.user.username,
            'content':message.message,
            'timestamp':str(message.date_add),
        }
        
    
    def new_message(self, data):
        print('new message')
        
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Chat.objects.create(
            user=author_user,
            message=data['message']
        )
        
        content = {
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    
    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message,
    }
    
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        
        self.commands[data['command']](self, data)
        
    def send_chat_message(self, message):
        
        # message = data['message']

        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))