from django import template

register = template.Library()

@register.filter
def times(number):
    try:
        return range(int(number) if number is not None else 0)
    except (ValueError, TypeError):
        return range(0)
    
@register.filter
def get_cuurect_price(price):
    try:
        discount = (price * 30) / 100
        return price - discount
    except (ValueError, TypeError):
        return price
    
@register.filter
def attr(obj, name):
    """Return dynamic attribute value from an object."""
    return getattr(obj, name, None)