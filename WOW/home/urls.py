from django.urls import path,include
from django.conf.urls import url
from home.views import *
from customer_portal import *

urlpatterns = [
    url(r'^$',home_page),
]
