from django import template

register = template.Library()

@register.filter
def get_list(lst, name):
    return lst.getlist(name)