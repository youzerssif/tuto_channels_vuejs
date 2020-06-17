from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from channels.auth import login 
from asgiref.sync import async_to_sync

# from .models import *

class ChatConsumerEditor(AsyncWebsocketConsumer):
    async def connect(self):
       
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_name = "hello"
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'] 
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
        #  # login the user to this session.
        # await login(self.scope, user)
        # # save the session (if the session backend does not access the db you can use `sync_to_async`)
        # await database_sync_to_async(self.scope["session"].save)()
        # async_to_sync(login)(self.scope, user)
        # self.scope["session"].save()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            
            'message': message ,
            
        }))

class ChatConsumer(AsyncWebsocketConsumer):
    
    

    
    async def connect(self):
        
        self.username = await database_sync_to_async(self.get_name)()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_name = "hello"
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
    def get_name(self):
        return User.objects.all()[0].name

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'] 
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            
            'message': message ,
            
        }))