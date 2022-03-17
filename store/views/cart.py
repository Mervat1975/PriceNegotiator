from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        print(products)
        get_data = request.GET
        if (get_data.get("flag") == "0" or get_data.get("flag") == "1"):
            flag = get_data.get("flag")

        else:
            flag = "99"
        return render(request, 'store/cart.html', {'flag': flag, 'products': products})
