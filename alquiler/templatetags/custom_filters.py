from django import template

register = template.Library()

@register.filter(name='boolean_to_text')
def boolean_to_text(value):
    return "Sí" if value else "No"

@register.filter
def dash_if_none(value):
    return value if value is not None and value != '' else '-'