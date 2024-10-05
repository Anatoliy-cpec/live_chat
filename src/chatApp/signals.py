from .models import Author
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


updating_username = False



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance, nickname=instance.username)
    else:
        # Если профиль уже существует, просто обновите его
        try:
            author = instance.author
            author.nickname = instance.username
            author.save()
        except Author.DoesNotExist:
            # Если по какой-то причине профиль не существует, создайте его
            Author.objects.create(user=instance, nickname=instance.username)


@receiver(post_delete, sender=User)
def delete_author_data(sender, instance, **kwargs):
    try:
        author = instance.author
        if author and not hasattr(instance, '_deleting'):
            author._deleting = True
            author.delete()
    except Author.DoesNotExist:
        pass

@receiver(post_delete, sender=Author)
def delete_user_data(sender, instance, **kwargs):
    try:
        user = instance.user
        if user and not hasattr(instance, '_deleting'):
            user._deleting = True
            user.delete()
    except User.DoesNotExist:
        pass

@receiver(post_save, sender=Author)
def change_user_nickname(sender, instance, **kwargs):
       global updating_username
       if instance.user.username != instance.nickname:
           try:
               User.objects.get(username=instance.nickname)
               # Либо пропустите обновление, либо измените nickname на уникальное значение
               return
           except ObjectDoesNotExist:
               updating_username = True
               instance.user.username = instance.nickname
               instance.user.save()
               updating_username = False
    
    