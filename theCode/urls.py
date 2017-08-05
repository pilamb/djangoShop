# -*- coding: utf-8 -*-

import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from clients.views import UserModelListView, UserModelDetailView, UserModelUpdateView, UserModelDeleteView
from notifications.views import NotificationListView, NotificationDetailView
from shop.views import OrderListView,\
    OrderDetailView,\
    OrderUpdateView,\
    OrderDeleteView, OrdersUserModelListView, SaleDetailView, SaleListView, \
OrdersUserModelListView, InvoicePDFModel, ShipmentDetailView
from events.views import EventListView
from warehouse.views import ProductsListView, ProductDetailView
from .views import create_order, create_user2, create_concrete_order
from customForms import index, contact, about, authenticate, panel, sitemap, cookies, sitemap, help, terms,info, shipments, \
passwordChange, search, salesGraphics, productsGraphics


admin.autodiscover()
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', index.page, name='index'),

                       url(r'^createUser$','theCode.views.create_user2.page',name='create_user'),
                       url(r'^listUsers/',UserModelListView.as_view(),name='users_list'),  # only ADMIN, for panel
    url(r'^detailUser/(?P<pk>\d+)/$', UserModelDetailView.as_view(), name='detail_user'),
                       url(r'^EditUser/(?P<pk>\d+)/$', UserModelUpdateView.as_view(), name='edit_user'),
                       url(r'^deleteUser/(?P<pk>\d+)/$', UserModelDeleteView.as_view(),name='delete_user'),
                       url(r'^changeCredentials/$', login_required(passwordChange.page), name='change_password'),

                       url(r'^createOrder2/(?P<pk>\d+)/$',login_required(create_concrete_order.page),name='create_order2'),  #se viene of haber elegido ya un modulo, pk
    url(r'^listOrders/',OrderListView.as_view(),name='listado_orders'),  #soloADMIN, para panel
    url(r'^detailOrder/(?P<pk>\d+)/$',OrderDetailView.as_view(),name='detail_order'),
                       url(r'^EditOrder/(?P<pk>\d+)/$', OrderUpdateView.as_view(),name='Edit_order'),
                       url(r'^deleteOrder/(?P<pk>\d+)/$', OrderDeleteView.as_view(),name='delete_order'),
                       url(r'^OrdersUser/',OrdersUserModelListView.as_view(),name='ordersUser'),  #para users normales

    url(r'^detailSale/(?P<pk>\d+)/$', SaleDetailView.as_view(), name='detail_sale'),
                       url(r'^chart_sales$', login_required(salesGraphics.page), name='chart_sales'),
                       url(r'^chart_products$', login_required(productsGraphics.page),name='chart_products'),

                       url(r'^notification/(?P<pk>\d+)/$', NotificationDetailView.as_view(), name='detail_notificacion'),
                       url(r'^messages/(?P<pk>\d+)/$', NotificationListView.as_view(), name='messages'),
                       url(r'^listMessage_classes/$', NotificationListView.as_view(), name='ListaMessage_classes'),

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
                       url(r'^events/', EventListView.as_view(), name='events'),

                       url(r'^result/$', search.page, name='result'),  # result searchs
    url(r'^detailShipment/(?P<pk>\d+)/$', ShipmentDetailView.as_view(),name='detail_shipment'),
                       url(r'^invoice/(?P<pk>\d+)/$', InvoicePDFModel.as_view(), name='imprimir_invoice'),

                       url(r'^panelUser/', login_required(panel.page), name='panel'),
                       url(r'^login/$', 'theCode.customForms.authenticate.login',name='login'),
                       url(r'^logout/$', login_required(authenticate.logout), name='logout'),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,
    }),
                       )
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
