# Generated by Django 3.2 on 2021-08-17 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dm', '0002_message_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.IntegerField(blank=True),
        ),
    ]
