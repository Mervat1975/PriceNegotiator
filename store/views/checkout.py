from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Products
from store.models.orders import Order

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


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
        orderlist = []
        order_details = "<table><tr><th>Product</th><th>Quantity</th><th>Price</th><th>Discount</th></tr>"
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
            order_details += "<tr><td>"+product.name+"</td>"
            order_details += "<td>"+str(cart.get(str(product.id)))+"</td>"
            order_details += "<td>"+str("{:.2f}".format(product.price))+"</td>"
            order_details += "<td>"+str("{:.2f}".format(float(product.price) *
                                        float(float(disc)/100)))+"</td></tr>"

            order.save()
            added_order = Order.objects.filter(
                customer=Customer(id=customer)).order_by('-id')[0]
            orderlist.append(str(added_order.id))
        orderlist_str = ",".join(orderlist)
        net = tot-tot_disc

        message = "<p>Your total amount is "
        message += str("{:.2f}".format(net))+"CAD . It was "
        message += str("{:.2f}".format(tot)) + " CAD"
        message += ". You saved "
        message += str("{:.2f}".format(tot_disc)) + \
            " CAD.</p>"
        message += order_details+"</table>"
        message += '<p> Please<a href="http://127.0.0.1:8000/confirm/?order_list='
        message += orderlist_str+'">Confirm </a> that your order is completed'
        message += '<p><strong> Thank You.</strong></p>'

        print('orderlist', *orderlist)
        request.session['cart'] = {}
        try:

            subject, from_email, to = 'The Store: Order Details',  'mervat.mustafa@dcmail.ca', email
            text_content = 'This is an important message.'
            html_content = message
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print(e)

        return redirect('cart')
