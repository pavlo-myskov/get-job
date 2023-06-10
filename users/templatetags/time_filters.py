from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter("timeago", is_safe=False)
def custom_timesince(value):
    """Custom timesince filter that returns only one unit of time."""
    if not value:
        return ''
    try:
        return timesince(value, depth=1)
    except (ValueError, TypeError):
        return ''
