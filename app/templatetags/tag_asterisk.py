from django import template

register = template.Library()


@register.simple_tag
def is_mandatory():
    return '<i class="glyphicon glyphicon-asterisk mandatory-sign"></i>'
