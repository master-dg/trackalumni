from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def dropdown_option(value, display_value, current):
    return mark_safe(
        f"<option value='{value}' {'selected' if str(value) == current else ''}>{display_value}</option>"
    )
