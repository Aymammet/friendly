# Generated by Django 3.2 on 2021-08-17 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dm', '0003_alter_message_message_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_id',
        ),
    ]
