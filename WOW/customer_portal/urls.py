from django.urls import path,include
from customer_portal.views import *
from django.conf.urls import url
from django.contrib import admin
admin.site.site_header = 'WOW Admin'
admin.site.site_title = 'dd'
admin.site.index_title = 'Welcome to WOW Admin Portal'



urlpatterns = [
    url(r'^index/$',index),
    url(r'^login/$',login),
    url(r'^auth/$',auth_view),
    url(r'^logout/$',logout_view),
    url(r'^register/$',register),
    url(r'^registration/$',registration),
    
    # url(r'^search/$',search),
    # url(r'^search_results/$',search_results),
    url(r'^rent/$',rent_vehicle),
    url(r'^confirmed/',confirm),
    url(r'^return/',return_vehicle),
    url(r'^return_detail/',return_detail),
    url(r'^invoice/',invoice),
    url(r'^pay/',pay),
    url(r'^pay_confirmed/',pay_confirmed),
    url(r'^profile/',profile),
    url(r'^invoice_failed/',invoice_failed),
    url('admin/', lambda x: HttpResponseRedirect('http://localhost:8000/admin/')),
    
    # url(r'^manage/',manage),
    # url(r'^update/',update_order),
    # url(r'^delete/',delete_order),
]
