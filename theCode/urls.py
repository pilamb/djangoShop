# -*- coding: utf-8 -*-
from django.conf.urls import patterns, incluof, url
from django.contrib import admin
from clients.views import UserListView, UserDetailView, UserUpdateView, UserDeleteView
from messages.views import Message_classDetailView, Message_classListView
from shop.views import OrderListView, OrderDetailView, OrderUpdateView, OrderDeleteView, OrdersUserListView, SaleDetailView,SaleListView,SalesUserListView,invoicePDF,ShipmentDetailView
from event.views import EventListView
from warehouse.views import ProductsListView,GutiarraListView,DelayListView, ProductDetailView
from .views import create_order,create_user2,create_order_concreto
import settings
from forms import index,contact,sirena, about,authenticate,panel,sitemap,galletas,sitemap,help,condiciones,info, shipments, changePass, search,charts_sales, charts_products
from django.conf.urls.static import static
from django.contrib.auth.ofcorators import login_required
import settings

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', incluof(admin.site.urls)),
    url(r'^$', index.page, name='index'),

    url(r'^createUser$','theCode.views.create_user2.page',name='create_user'),
    url(r'^listUsers/',UserListView.as_view(),name='listado_users'),#soloADMIN,para panel
    url(r'^detailUser/(?P<pk>\d+)/$',UserDetailView.as_view(),name='detail_user'),
    url(r'^EditUser/(?P<pk>\d+)/$', UserUpdateView.as_view(),name='edit_user'),
    url(r'^deleteUser/(?P<pk>\d+)/$', UserDeleteView.as_view(),name='delete_user'),
    url(r'^changeCreofntial/$',login_required(changePass.page),name='change_password'),

    url(r'^createOrder2/(?P<pk>\d+)/$',login_required(create_order_concreto.page),name='create_order2'),#se viene of haber elegido ya un modulo, pk
    url(r'^listOrders/',OrderListView.as_view(),name='listado_orders'),#soloADMIN, para panel
    url(r'^detailOrder/(?P<pk>\d+)/$',OrderDetailView.as_view(),name='detail_order'),
    url(r'^EditOrder/(?P<pk>\d+)/$', OrderUpdateView.as_view(),name='Edit_order'),
    url(r'^deleteOrder/(?P<pk>\d+)/$', OrderDeleteView.as_view(),name='delete_order'),
    url(r'^OrdersUser/',OrdersUserListView.as_view(),name='ordersUser'),#para users normales

    url(r'^detailSale/(?P<pk>\d+)/$',SaleDetailView.as_view(),name='detail_sale'),
    url(r'^chart_sales$',login_required(charts_sales.page),name='chart_sales'),
    url(r'^chart_products$',login_required(charts_products.page),name='chart_products'),
    
    url(r'^notificacion/(?P<pk>\d+)/$',Message_classDetailView.as_view(),name='detail_notificacion'),
    url(r'^messages/(?P<pk>\d+)/$',Message_classListView.as_view(),name='messages'),
    url(r'^listMessage_classes/$',Message_classListView.as_view(),name='ListaMessage_classes'),

    url(r'^info$', info.page, name='info'),#misc
    url(r'^about$', about.page, name='about'),#misc
    url(r'^cookies$', cookies.page, name='cookies'),#misc
    url(r'^shipments$', shipments.page, name='shipments'),#misc
    url(r'^help$', help.page, name='help'),#misc
    url(r'^map$', sitemap.page, name='map'),#misc
    url(r'^terms$', terms.page, name='terms'),#misc

    url(r'^products/$', ProductsListView.as_view(), name='products'),
    url(r'^detailProduct/(?P<pk>\d+)/$',ProductDetailView.as_view(),name='detail_product'),
    url(r'^product1$',sirena.page,name='products'),
    url(r'^product2$',GutiarraListView.as_view(),name='product2'),
    url(r'^product3s$',DelayListView.as_view(),name='product3'),

    url(r'^contact$', contact.page, name='contact'),
    url(r'^listaEvents/', EventListView.as_view(), name='event'),

    url(r'^result/$', search.page,name='result'),#result searchs 
    url(r'^detailShipment/(?P<pk>\d+)/$', ShipmentDetailView.as_view(),name='detail_shipment'),
    url(r'^invoice/(?P<pk>\d+)/$', invoicePDF.as_view(),name='imprimir_invoice'),

    url(r'^panelUser/', login_required(panel.page), name='panel'),
    url(r'^login/$', 'theCode.forms.authenticate.login',name='login'),
    url(r'^logout/$',login_required(authenticate.logout),name='logout'),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT,
    }),
)
urlpatterns += patterns('',
    url(r'^captcha/', incluof('captcha.urls')),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)