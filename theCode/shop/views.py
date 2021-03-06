# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic import DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django_fsm_log.models import StateLog
from easy_pdf.views import PDFTemplateView
from datetime import date

from theCode.views.create_order import NewProductOrderForm
from warehouse.models import Product
from notifications.models import Notification
from clients.models import UserModel
from models import Order, Sale, Shipment


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *args):
        view = super(LoginRequiredMixin, cls).as_view(*args)
        return login_required(view)


class OrderListView(LoginRequiredMixin, ListView):
    """This view is only for admins?"""
    model = Order
    template_name = "shop/orders_list.html"
    paginate_by = 3

    def get_context_data(self, *args):
            context = super(OrderListView, self).get_context_data(*args)
            return context


class OrdersUserModelListView(LoginRequiredMixin, ListView):
    """
    List of orders for just one user
    """
    template_name = "shop/order_list_for_user.html"
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, *args):
        context = super(OrdersUserModelListView, self).get_context_data(*args)
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "shop/order_detail.html"

    def get_context_data(self, **kwargs):
            context = super(OrderDetailView, self).get_context_data(**kwargs)
            if not self.request.user.is_super:
                try:
                    nots = Notification.objects.filter(user=self.request.user)
                except Notification.DoesNotExist:
                    nots = ()
                try:
                    states = StateLog.objects.filter(object_id=self.object.id)
                except StateLog.DoesNotExist:
                    states = ""
                try:
                    shipments = Shipment.objects.get(order= self.object.id)
                except Shipment.DoesNotExist:
                    shipments = ""
                context['Notification'] = nots
                context['H'] = states
                context['shipment'] = shipments
            return context

    def get_queryset(self):
        if not self.request.user.is_super:
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.all()


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['paid', 'module', ]
    template_name = "shop/order_edit.html"
    success_url = reverse_lazy('panel')

    def clean(self):
        super(OrderUpdateView, self).clean()

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(OrderUpdateView, self).post(request, *args, **kwargs)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """
    State to cancel and get on sale available again
    """
    model = Order
    template_name = "shop/order_confirm_delete.html"
    success_url = reverse_lazy('panel')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            self.object = self.get_object()
            self.object.state = 'ca'
            self.object.save()
            m = Product.objects.get(pk=self.object.module.id)
            m.on_sale = True
            m.save()
            messages.warning(request,
                             'Order marked as cancelled <b>correctly</b>.')
            # Notify
            return HttpResponseRedirect(reverse_lazy('index'))


class SaleListView(LoginRequiredMixin, ListView):
    """
    View for ADMIN for all sales
    """
    model = Sale
    template_name = "shop/orders_list.html"
    paginate_by = 5
    # def get_queryset(self):
    #     return Sale.objects.all()

    def get_context_data(self, **kwargs):
            context = super(SaleListView, self).get_context_data(**kwargs)
            return context


class SalesUserModelListView(LoginRequiredMixin, ListView):
    """
    Sales list for users
    """
    template_name = "shop/orders_list.html"

    def get_queryset(self):
        return Sale.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
            context = super(SalesUserModelListView, self).\
                get_context_data(**kwargs)
            return context


class SaleDetailView(LoginRequiredMixin, DetailView):
    """
    Detail of each Sale
    """
    model = Sale
    template_name = "sale_detail.html"

    def get_context_data(self, **kwargs):
            context = super(SaleDetailView, self).get_context_data(**kwargs)
            order = Order.objects.get(sale=self.object)
            context['order'] = order
            return context

    def get_queryset(self):
        if not self.request.user.is_super:
            return Sale.objects.filter(pk=
                                       Order.objects.filter(
                                           user=self.request.user))
        else:
            return Sale.objects.all()


class ShipmentDetailView(LoginRequiredMixin, DetailView):
    order = Shipment
    template_name = "shop/order_detail.html"

    def get_context_data(self, **kwargs):
            context = super(ShipmentDetailView, self).\
                get_context_data(**kwargs)
            return context

    def get_queryset(self):
        if not self.request.user.is_super: 
            return Shipment.objects.filter(order=Order.objects.filter(
                user=self.request.user))
        else:
            return Shipment.objects.all()
            

class InvoicePDFModel(LoginRequiredMixin, PDFTemplateView):
    """
    Generator of invoices to PDF format
    """
    template_name = "shop/pdf_invoice.html"

    def get_context_data(self, **kwargs):
        context = super(InvoicePDFModel, self).get_context_data(**kwargs)
        try:
            u = get_object_or_404(UserModel, pk=self.request.user.id)
            context['user'] = u
            ped = get_object_or_404(Order, pk=context['pk'])
            context['order'] = ped
            sale = Sale.objects.get(code=ped.code_ingreso)
            context['sale'] = sale
            shipment = Shipment.objects.get(order_id=ped.id)
            context['shipment'] = shipment
            context['today'] = date.today()
            context['pagesize'] = "A4",
            context['title'] = "INVOICE",
            pe = shipment.shipment_price
            pp = sale.price
            context['total'] = pe + pp
            return context
        except ObjectDoesNotExist:
            #  TODO: logger.error("Error on shipment {0}")
            raise Exception
