from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


from django.views.generic import (
    TemplateView, DetailView, UpdateView, CreateView, DeleteView
)

from .models import Author, Chat, ChatRoom, Message

from .forms import AuthorEditForm

class ChatHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.get_queryset().order_by('id')
        context['rooms'] = ChatRoom.objects.get_queryset().order_by('id')
        context['author'] = self.request.user.author
        return context
    
def chat_create(request, to_author_id:int, **kwargs):
    __have = True
    if request.method == 'POST':
        print('post')
        message = request.POST.get('message', '')
        print(message)
        if message is None or message == '':
            print('empty')
            return redirect('users/')
        else:
            print('no empty')

            chats = Chat.objects.all()

            if chats:
                for chat in chats:

                    print(chat)

                    if (chat.user_from.id == request.user.author.id and chat.user_to.id == to_author_id) or (chat.user_to.id == request.user.author.id and chat.user_from.id == to_author_id):
                        newMessage = Message.objects.create(author=request.user.author, text=message)
                        newMessage.save()
                        chat.messages.add(newMessage)
                        print('already have')
                        __have = True
                        return redirect(f'/chat/{chat.id}')
                    else:
                        __have = False
            else:
                print('empty chats')
                __have = False

        if not __have:
            print('dont have')
            author = Author.objects.get(id=to_author_id)
            newChat = Chat.objects.create(user_from=request.user.author, user_to=author)
            newMessage = Message.objects.create(author=request.user.author, text=message)
            newMessage.save()
            newChat.messages.add(newMessage)
            newChat.save()
            return redirect(f'/chat/{newChat.id}')  
        
    return HttpResponseNotAllowed(['POST'])

class ChatDetailsView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat_details.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.get_queryset().order_by('id')
        context['rooms'] = ChatRoom.objects.get_queryset().order_by('id')
        context['room_id'] = self.kwargs['pk']
        context['author'] = self.request.user.username
        return context

class ChatRoomDetailsView(LoginRequiredMixin, DetailView):
    model = ChatRoom
    template_name = 'chat_room_details.html'
    context_object_name = 'chat_room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.get_queryset().order_by('id')
        context['room'] = self.get_object()
        context['room_id'] = self.kwargs['pk']
        context['author'] = self.request.user.username
        return context
    
class UsersView(LoginRequiredMixin, TemplateView):
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.get_queryset().order_by('id')
        context['rooms'] = ChatRoom.objects.get_queryset().order_by('id')

        context['authors'] = Author.objects.all()

        return context

class AuthorUpdate(  LoginRequiredMixin,
                            UpdateView):
    form_class = AuthorEditForm
    model = Author
    context_object_name = 'Author'
    queryset = Author.objects.get_queryset().order_by('id')
    template_name = 'Author_edit.html'
    success_url = 'http://127.0.0.1:8000/chat/home/'

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        author = self.get_object()
        user = request.user
        if not (author.user == user or user.is_superuser):
            raise PermissionDenied
        return handler

class ChatRoomEditView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_room_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.get_queryset().order_by('id')
        context['room'] = ChatRoom.objects.get(id=context['pk'])
        context['room_id'] = self.kwargs['pk']
        context['author'] = self.request.user.author
        return context
    
class ChatRoomCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'chat_room_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = Chat.objects.get_queryset().order_by('id')
        context['rooms'] = ChatRoom.objects.get_queryset().order_by('id')
        context['author'] = self.request.user.author
        context['author_id'] = self.request.user.id
        context['authors'] = Author.objects.get_queryset().order_by('id')
        return context
