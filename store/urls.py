from django.contrib import admin
from django.urls import path
from store.views.home import Index, store
from store.views.signup import Signup
from store.views.login import Login, logout
from store.views.cart import Cart
from store.views.confirm_order import Confirm
from store.views.checkout import CheckOut
from store.views.runbot import RunBot
from store.views.orders import OrderView
from store.middlewares.auth import auth_middleware
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),

    path('confirm/',
         Confirm.as_view(), name='confirm'),

    path('check-out', CheckOut.as_view(), name='checkout'),
    path('run-bot', RunBot.as_view(), name='runbot'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
