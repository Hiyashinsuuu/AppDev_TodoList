# filepath: /C:/Users/Admin/Desktop/tpg/todo/todoprj/todoapp/templatetags/custom_tags.py
from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return timezone.localtime(timezone.now()).strftime(format_string)