# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from warehouse.views import ProductsListView, ProductDetailView
from .views import create_order, create_user2, create_concrete_order
from customForms import index, contact, about, authenticate, panel,\
    sitemap, cookies, sitemap, help, terms,info, shipments, \
    passwordChange, search, salesGraphics, productsGraphics

admin.autodiscover()
urlpatterns = []
urlpatterns += [
        url(r'^admin/', include(admin.site.urls)),
        url(r'account/', include('clients.urls', namespace='account')),
        url(r'shop/', include('shop.urls', namespace='shop')),
        url(r'^events/', include('events.urls', namespace='events')),
        url(r'^$', index.page, name='index'),

        url(r'^createUser$', 'theCode.views.create_user2.page',
            name='create_user'),
        # only ADMIN, for panel
        url(r'^changeCredentials/$', login_required(passwordChange.page),
            name='change_password'),
        url(r'^createOrder2/(?P<pk>\d+)/$',
            login_required(create_concrete_order.page),
            name='create_order2'),
        # this creates an order when a product has already been chosen

        url(r'^chart_sales$',
            login_required(salesGraphics.page), name='chart_sales'),
        url(r'^chart_products$',
            login_required(productsGraphics.page), name='chart_products'),

        url(r'^info$', info.page, name='info'),  #misc
        url(r'^about$', about.page, name='about'),  #misc
        url(r'^cookies$', cookies.page, name='cookies'),  #misc
        url(r'^shipments$', shipments.page, name='shipments'),  #misc
        url(r'^help$', help.page, name='help'),  #misc
        url(r'^map$', sitemap.page, name='map'),  #misc
        url(r'^terms$', terms.page, name='terms'),  #misc
        url(r'^products/$', ProductsListView.as_view(), name='products'),
        # url(r'^product2/$', Product2DetailView.as_view(), name='product2'),
        url(r'^detailProduct/(?P<pk>\d+)/$', ProductDetailView.as_view(),
            name='detail_product'),
        # url(r'^products1$', ProductView.as_view(), name='product3'),
        url(r'^contact$', contact.page, name='contact'),
        url(r'^result/$', search.page, name='result'),  # search results

        url(r'^panelUser/', login_required(panel.page), name='panel'),
        url(r'^login/$', 'theCode.customForms.authenticate.login',
            name='login'),
        url(r'^logout/$', login_required(authenticate.logout), name='logout'),

]


