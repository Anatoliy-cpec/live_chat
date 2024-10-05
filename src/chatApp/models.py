from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(default='images/no_avatar.jpg', blank=True, null=True, upload_to='images/%Y/%m/%d/')
    nickname = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.nickname

class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.CharField(max_length=64, blank=False, null=False, default='message')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-creation_date']
    def __str__(self) -> str:
        return f'{self.author}: {self.text}'
    
    def last_10_messages(self):
        return Message.objects.order_by('-creation_date').all()[:10]

    
class Chat(models.Model):
    user_from = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='from_user')
    user_to = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='to_user')

    messages = models.ManyToManyField(Message)

    def is_user_in(self, author):
        return self.user_from == author or self.user_to == author
    
    def add_message(self, message):
        self.messages.add(message)
        self.save()


    def __str__(self) -> str:
        return f'{self.user_from} to {self.user_to}'

class ChatRoom(models.Model):
    name = models.CharField(max_length=20, default='Group chat', unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, related_name='owner')
    users = models.ManyToManyField(Author, blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def add_message(self, message):
        self.messages.add(message)
        self.save()


    def __str__(self) -> str:
        return self.name


