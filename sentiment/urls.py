from django.contrib import admin
from django.urls import path
from django.conf import settings
from sentiment.views.signup import Signup
from sentiment.views.review import Review
from sentiment.views.login import Login, logout
from sentiment.views.home import home, review_submission
from django.conf.urls import url
from django.urls import include, path
from sentiment.middlewares.auth import auth_middleware


from django.conf.urls.static import static

import sentiment

urlpatterns = [
    path('', auth_middleware(home), name='admin_homepage'),
    path('signup', Signup.as_view(), name='admin_signup'),
    path('login', Login.as_view(), name='admin_login'),
    path('logout', logout, name='admin_logout'),
    path('review', Review.as_view(), name='review'),
    path('review_submission', review_submission, name='review_submission'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
