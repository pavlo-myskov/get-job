from django import template
from copy import deepcopy

register = template.Library()


@register.filter
def update_placeholder(field, placeholder):
    """Update the placeholder attribute of the widget"""
    # deepcopy is used to avoid changing the original field globally
    new_field = deepcopy(field)
    new_field.field.widget.attrs.update({'placeholder': placeholder})
    return new_field
