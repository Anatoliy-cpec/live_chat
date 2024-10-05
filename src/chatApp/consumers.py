import json
from datetime import datetime
from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message, Chat, ChatRoom


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['author']
        room_id = self.scope["url_route"]["kwargs"]["room_id"]

        room = Chat.objects.get(pk=room_id)

        if data['message'] == '':
            return

        author_user = User.objects.get(username=author)
        message = Message.objects.create(
            author=author_user.author,
            text=data['message'],
        )
        room.add_message(message)
        content = {
            'command': 'new_message',
            'avatar_url': author_user.author.profile_photo.url,
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []

        for message in messages:
            result.append(self.message_to_json(message))

        return result

    def message_to_json(self, message):
        __date = str(message.creation_date).split('+')[0]
        date = datetime.strptime(__date, '%Y-%m-%d %H:%M:%S.%f')
        date = date.strftime('%d-%m-%y:%H:%M')
        return {
            "author": message.author.user.username,
            "text": message.text,
            "creation_date": date,
        }

    commands = {

        'fetch_messages': fetch_messages,
        'new_message': new_message,

    }



    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)


    def send_chat_message(self, message):

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
        
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        async_to_sync(self.send(text_data=json.dumps(message)))

class ChatRoomConsumer(WebsocketConsumer):

    def new_message(self, data):
        author = data['author']
        room_id = self.scope["url_route"]["kwargs"]["room_id"]

        room = ChatRoom.objects.get(pk=room_id)

        if data['message'] == '':
            return

        author_user = User.objects.get(username=author)
        message = Message.objects.create(
            author=author_user.author,
            text=data['message'],
        )
        room.add_message(message)
        content = {
            'command': 'new_message',
            'avatar_url': author_user.author.profile_photo.url,
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []

        for message in messages:
            result.append(self.message_to_json(message))

        return result

    def message_to_json(self, message):
        __date = str(message.creation_date).split('+')[0]
        date = datetime.strptime(__date, '%Y-%m-%d %H:%M:%S.%f')
        date = date.strftime('%d-%m-%y:%H:%M')
        return {
            "author": message.author.user.username,
            "text": message.text,
            "creation_date": date,
        }

    commands = {

        'new_message': new_message,

    }



    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)


    def send_chat_message(self, message):

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
        
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        async_to_sync(self.send(text_data=json.dumps(message)))       