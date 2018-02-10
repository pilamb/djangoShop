from django.conf.urls import url


from .views import SaleDetailView, OrderDeleteView, \
    OrderListView, OrdersUserModelListView, OrderDetailView, OrderUpdateView,\
    ShipmentDetailView, InvoicePDFModel


urlpatterns = [
    url(
        # only for admins
        regex=r'^listOrders/',
        view=OrderListView.as_view(),
        name='orders_list',
    ),
    url(
        regex=r'^detailOrder/(?P<pk>\d+)/$',
        view=OrderDetailView.as_view(),
        name='order_detail',
    ),
    url(
        regex=r'^EditOrder/(?P<pk>\d+)/$',
        view=OrderUpdateView.as_view(),
        name='order_edit',
    ),
    url(
        regex=r'^deleteOrder/(?P<pk>\d+)/$',
        view=OrderDeleteView.as_view(),
        name='order_delete',
    ),
    url(
        regex=r'userOrders',
        view=OrdersUserModelListView.as_view(),
        name='user_orders',
    ),
    url(
        regex=r'^detailSale/(?P<pk>\d+)/$',
        view=SaleDetailView.as_view(),
        name='sale_detail',
    ),
    url(
        regex=r'^detailShipment/(?P<pk>\d+)/$',
        view=ShipmentDetailView.as_view(),
        name='shipment_detail',
    ),
    url(
        regex=r'^invoice/(?P<pk>\d+)/$',
        view=InvoicePDFModel.as_view(),
        name='print_invoice',
    ),
]
