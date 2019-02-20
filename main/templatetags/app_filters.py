from django import template

register = template.Library()

@register.filter(name='range')
def range(min=5):
    return range(min)
