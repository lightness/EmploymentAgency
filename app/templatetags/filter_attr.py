from django import template
register = template.Library()


@register.filter(name='attr', is_safe=False)
def get_attr(obj, args):
    splitargs = args.split(',')
    try:
        (attribute, default) = splitargs
    except ValueError:
        (attribute, default) = args, ''

    try:
        try:
            attr = obj.__getattribute__(attribute)
        except AttributeError:
            attr = obj.__dict__.get(attribute, default)
    except Exception:
        attr = default

    if hasattr(attr, '__call__'):
        return attr.__call__()
    else:
        return attr
