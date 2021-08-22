from django import template
from notifications.models import Notification

register = template.Library()


@register.inclusion_tag('show_notifications2.html', takes_context=True)


def show_notifications2(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(receiver=request_user).exclude(user_has_seen=True).order_by('-date')
    return {'notifications':notifications}

