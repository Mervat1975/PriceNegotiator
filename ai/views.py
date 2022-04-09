import json

from django.shortcuts import render
from store.models import discount
from store.models.discount import Discount

import store.templatetags.cart
from .components.chatbot import chatbot_response
from django.http import HttpResponse
from store.models import *


def main_view(request):

    current_customer = Customer.get_customer_by_id(
        request.session.get('customer'))
    cart = request.session.get('cart')
    products = Products.get_products_by_id(list(cart.keys()))
    amount = store.templatetags.cart.total_cart_price(products, cart)
    discount_range = Discount.get_discount_all()
    min_disc = 0.0
    max_disc = 0.0

    for disc in discount_range:
        if disc.amount_from <= int(amount):
            if disc.amount_to > int(amount):
                min_disc = disc.discount_from
                max_disc = disc.discount_to
    discount = 0.00
    if request.method == 'POST':

        response = {'status': None, 'message': None}
        user_response = json.loads(request.body)

        user_response = user_response['message']

        if(user_response == "Yes"):
            request.session['accept_flag'] = 1
        ai_response = chatbot_response(user_response)
        request.session['offer_no'] = request.session['offer_no']+1

        response['message'] = {'text': ai_response, 'offer_no': str(request.session['offer_no']),
                               'min_disc':  str(min_disc), 'max_disc': str(max_disc), 'amount': str(amount), 'user_response': user_response, 'accept_flag': str(request.session['accept_flag'])}
        return HttpResponse(json.dumps(response))

    else:
        get_data = request.GET
        if (get_data.get("flag") == "0" or get_data.get("flag") == "1"):
            flag = get_data.get("flag")

        else:
            flag = "99"
        request.session['accept_flag'] = 0
        request.session['offer_no'] = 0
        discount = get_data.get("discount")
        if (discount is None):
            discount = 0.0

        return render(request, "bot-index.html", {'flag': flag, 'products': products,
                                                  'customer': current_customer, 'cart': cart, 'min_disc': min_disc,
                                                  'max_disc': max_disc, 'amount': amount, 'discount': discount})
