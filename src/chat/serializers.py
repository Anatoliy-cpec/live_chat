from rest_framework import serializers
from chatApp.models import Author, Message, Chat, ChatRoom


class AuthorSerializer(serializers.ModelSerializer):
       class Meta:
           model = Author
           fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
       class Meta:
           model = Message
           fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
       class Meta:
           model = Chat
           fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
       class Meta:
           model = ChatRoom
           fields = '__all__'