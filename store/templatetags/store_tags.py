from django import template

register = template.Library()

@register.filter
def sum_items_price(items):
    """計算購物車所有項目的總金額，考慮折扣價"""
    return sum(item.get_subtotal() for item in items)