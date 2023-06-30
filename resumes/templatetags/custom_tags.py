from django import template

register = template.Library()


# Code snippet from: https://stackoverflow.com/a/63579304/20143678
@register.simple_tag
def define(val=None):
    """Define a variable in a template.

    Example:
    >>> {% define "my_value" as variable %}
    >>> {{ variable }}
    my_value
    """
    return val
