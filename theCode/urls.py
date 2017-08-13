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
        url(r'^$', index.page, name='index'),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^events/', include('events.urls', namespace='events')),
        # User related
        url(r'^login/$', 'theCode.customForms.authenticate.login',
            name='login'),
        url(r'^logout/$', login_required(authenticate.logout),
            name='logout'),
        url(r'account/', include('clients.urls', namespace='account')),
        url(r'^panelUser/', login_required(panel.page), name='panel'),
        url(r'^createUser$', 'theCode.views.create_user2.page',
            name='create_user'),
        url(r'^changeCredentials/$', login_required(passwordChange.page),
            name='change_password'),
        # Products/Shop
        url(r'shop/', include('shop.urls', namespace='shop')),
        url(r'^products/$', ProductsListView.as_view(), name='products'),
        url(r'^detailProduct/(?P<pk>\d+)/$', ProductDetailView.as_view(),
            name='detail_product'),
        url(r'^createOrder2/(?P<pk>\d+)/$',
            login_required(create_concrete_order.page),
            name='create_order2'),
        # this creates an order when a product has already been chosen
        # Charts about sales/expenses and products/visits. 4 Admins
        url(r'^chart_sales$',
            login_required(salesGraphics.page), name='chart_sales'),
        url(r'^chart_products$',
            login_required(productsGraphics.page), name='chart_products'),
        # miscellaneous/information
        url(r'^info$', info.page, name='info'),
        url(r'^about$', about.page, name='about'),
        url(r'^cookies$', cookies.page, name='cookies'),
        url(r'^shipments$', shipments.page, name='shipments'),
        url(r'^help$', help.page, name='help'),
        url(r'^map$', sitemap.page, name='map'),
        url(r'^terms$', terms.page, name='terms'),
        # Contact Form
        url(r'^contact$', contact.page, name='contact'),
        # Search results
        url(r'^result/$', search.page, name='result'),
]

urlpatterns += (
    url(r'^captcha/', include('captcha.urls')),
)
