from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Products
from store.models.orders import Order

from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        disc = 0.0
        try:
            disc = request.POST.get('discount')[0: -1]
        except:
            disc = 0.0

        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products, disc)
        tot = 0.0
        tot_disc = 0.0
        net = 0.0
        for product in products:
            tot += product.price * int(cart.get(str(product.id)))

            tot_disc += (float(product.price) * float(float(disc)/100)
                         ) * int(cart.get(str(product.id)))

            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          discount=float(product.price) *
                          float(float(disc)/100),
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        net = tot-tot_disc
        message = "Your total amount is "
        message += str("{:.2f}".format(net))+"CAD . It was "
        message += str("{:.2f}".format(tot)) + " CAD"
        message += ". You saved "
        message += str("{:.2f}".format(tot_disc)) + " CAD. Thank You"

        request.session['cart'] = {}
        try:
            send_mail(
                'The Store: Order Details',
                message,
                'mervat.mustafa@dcmail.ca',
                [email, 'em_me75@yahoo.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(e)

        return redirect('cart')
