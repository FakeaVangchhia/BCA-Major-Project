from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    """
    Multiply the value by the argument.
    """
    return value * arg
