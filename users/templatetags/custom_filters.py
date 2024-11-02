from django import template

register = template.Library()

@register.filter
def currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")