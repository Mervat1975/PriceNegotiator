from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.orders import Order
from django.views import View


class Confirm(View):
    def get(self, request):
        ids_str = request.GET.get('order_list', None).split(',')
        ids = []
        for id in ids_str:
            ids.append(int(id))

        orders = Order.get_orders_by_id(ids)
        for order in orders:
            order.status = True
            order.save()

        print("xxxx", orders)
        return render(request, 'store/confirm.html', {'orders': orders})
