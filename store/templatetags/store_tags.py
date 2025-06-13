from django import template

register = template.Library()

@register.filter
def sum_items_price(items):
    return sum(item.get_subtotal() for item in items)