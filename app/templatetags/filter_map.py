from django import template
register = template.Library()


@register.filter(name='map', is_safe=False)
def filter_map(obj, field):
    def extract(o):
        return getattr(o, field)

    try:
        attr = map(extract, obj)
    except Exception:
        attr = obj

    return attr
