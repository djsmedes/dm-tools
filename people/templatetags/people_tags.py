from django import template

register = template.Library()


@register.filter
def get_attr(obj, accessor):
    if hasattr(obj, accessor):
        return getattr(obj, accessor)
    else:
        return ''
