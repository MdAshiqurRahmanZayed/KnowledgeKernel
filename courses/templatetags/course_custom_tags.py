from django import template
register = template.Library()
import math


# 100 -> 10% --> mrp  - ( mrp * discount * 0.01 ) = selprice
@register.simple_tag
def course_sell_price(price,discount):
     if discount is None or discount == 0:
          return price 
     sell_price = price - (price*discount*.01)
     return math.ceil(sell_price)

@register.filter
def dollar(price):
     return f'${price}'
     