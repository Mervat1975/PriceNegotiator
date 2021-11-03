from django.shortcuts import render, redirect, HttpResponseRedirect

import ai.views
from store.models.product import Products
from store.models.category import Category
from django.views import View


class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if product:
            if cart:
                quantity = cart.get(product)
                if quantity:
                    if remove:
                        if quantity <= 1:
                            cart.pop(product)
                        else:
                            cart[product] = quantity - 1
                    else:
                        cart[product] = quantity + 1

                else:
                    cart[product] = 1
            else:
                cart = {product: 1}
        else:
            return ai.views.main_view(request)

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        print('reroute worked')
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    categories = Category.get_all_categories()
    category_id = request.GET.get('category')
    if category_id:
        products = Products.get_all_products_by_categoryid(category_id)
    else:
        products = Products.get_all_products()

    data = {'products': products, 'categories': categories}

    # print('you are : ', request.session.get('email'))
    print('you are : ', request.session.get('customer'))
    return render(request, 'store/index.html', data)
