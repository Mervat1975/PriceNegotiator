from django import template

register = template.Library()


@register.filter(name='currency')
def currency(number):
    return "CAD "+str(number)


@register.filter(name='multiply')
def multiply(number, number1):
    return number * number1


@register.filter(name='sub')
def sub(number, number1):
    return number - number1
