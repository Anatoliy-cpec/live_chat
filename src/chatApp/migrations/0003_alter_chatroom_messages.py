# Generated by Django 5.1 on 2024-09-19 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatApp', '0002_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='messages',
            field=models.ManyToManyField(blank=True, to='chatApp.message'),
        ),
    ]
