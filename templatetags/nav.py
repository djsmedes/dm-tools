from django import template

register = template.Library()


@register.filter
def create_breadcrumb(href, text):
    return {'href': href, 'text': text}
