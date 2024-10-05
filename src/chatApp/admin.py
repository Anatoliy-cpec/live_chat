from django.contrib import admin
from .models import Author, Chat, ChatRoom, Message

# Register your models here.


register = admin.site.register(Author)
register = admin.site.register(Chat)
register = admin.site.register(ChatRoom)
register = admin.site.register(Message)

