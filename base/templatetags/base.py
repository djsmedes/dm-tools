from django import template

register = template.Library()


@register.filter
def get_attr(obj, accessor):
    if hasattr(obj, accessor):
        return getattr(obj, accessor)
    else:
        return ''


@register.filter
def print_type_and_return(value):
    print(type(value))
    return value


@register.filter
def print_and_return(value):
    print(value)
    return value


@register.simple_tag
def val_in_iterable_in_dict_under_key(val, _dict, key):
    if _dict.get(key):
        _iterable = _dict[key]
        for item in _iterable:
            if str(item) == str(val):
                return True
    return False


@register.filter
def multiply(value, arg):
    return value * arg
