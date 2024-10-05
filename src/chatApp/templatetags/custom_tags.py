
from django import template
from django.urls import reverse
import os
from chatApp.models import Chat


register = template.Library()




@register.simple_tag
def is_user_in(chat, author):
    if chat.is_user_in(author):
       return True
    else:
        return False

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

