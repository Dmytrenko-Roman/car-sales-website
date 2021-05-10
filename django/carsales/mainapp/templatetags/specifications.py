from django import template

register = template.Library()

@register.filter
def product_spec(product):
    print(product)
    pass