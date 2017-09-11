from django import template
from django.conf import settings
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_user(pk, attr):
    obj = getattr(User.objects.get(pk=int(pk)), attr)
    return obj