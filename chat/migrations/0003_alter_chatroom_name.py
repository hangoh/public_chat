# Generated by Django 4.0.3 on 2022-03-16 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatroom_connection_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
