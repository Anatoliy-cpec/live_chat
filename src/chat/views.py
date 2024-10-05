from django.shortcuts import render
from django.shortcuts import redirect
import requests

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import AuthorSerializer, MessageSerializer, ChatSerializer, ChatRoomSerializer

from chatApp.models import *


from django.views.generic import (
    TemplateView
)



class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chat/home/')
        else:
            return super().get(request)
        
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        chatroom = self.get_object()
        user_id = request.user.author.id
        try:
            user = Author.objects.get(pk=user_id)
            chatroom.users.add(user)
            chatroom.save()
            return Response({'status': 'user added'}, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({'status': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
    def update_name(self, request, pk=None):
        chatroom = self.get_object()
        new_name = request.data.get('body')
        if new_name:
            chatroom.name = new_name
            chatroom.save()
            return Response({'status': 'name updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'name not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_room(self, request, pk=None):
        chatroom = self.get_object()
        chatroom.delete()
        return Response({'status': 'room deleted'}, status=status.HTTP_204_NO_CONTENT)        
        
