
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def is_orador_da_sessao(user, sessao):
    return sessao.oradores.filter(email=user.email).exists()