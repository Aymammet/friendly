# Generated by Django 3.2 on 2021-08-17 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dm', '0004_remove_message_message_id'),
        ('notifications', '0003_notification_thread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='thread',
        ),
        migrations.AddField(
            model_name='notification',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dm.room'),
        ),
    ]
