
from django.urls import path



from .views import (
    ChatHomeView, ChatDetailsView, UsersView, AuthorUpdate, ChatRoomDetailsView, ChatRoomEditView, ChatRoomCreateView, chat_create,

)


urlpatterns = [
    path('home/', ChatHomeView.as_view(), name='home'),

    path('<int:pk>', ChatDetailsView.as_view(), name='chat_detail'),
    
    path('<int:to_author_id>/', chat_create, name='chat_create'),

    path('room/<int:pk>/', ChatRoomDetailsView.as_view(), name='chat_room_detail'),
    path('users/', UsersView.as_view(), name='users'),
    path('author/<int:pk>', AuthorUpdate.as_view(), name='edit_author'),
    path('room/edit/<int:pk>', ChatRoomEditView.as_view(), name='chat_room_edit'),
    path('room/create/', ChatRoomCreateView.as_view(), name='chat_room_create'),
    
]

