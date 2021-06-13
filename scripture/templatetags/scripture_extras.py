from django import template
from django.template.defaultfilters import stringfilter

NUMBER_MAP = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "٤",
    "5": "٥",
    "6": "٦",
    "7": "٧",
    "8": "۸",
    "9": "۹"
}

register = template.Library()


@register.filter(name='arnum')
@stringfilter
def translate_ar_numeral(value):
    try:
        return "".join([NUMBER_MAP[char] for char in value])
    except KeyError:
        return value
