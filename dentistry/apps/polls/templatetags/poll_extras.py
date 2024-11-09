from django import template
from jalali_date import datetime2jalali


register = template.Library()
@register.filter(name="cut")
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")

@register.filter(name="show_jalali_datetime")
def jalali_datetime(value):
    return datetime2jalali(value).strftime('%y/%m/%d _ %H:%M')
