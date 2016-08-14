# -*- coding: utf-8 -*-
from proyecto.clients.models import Usuario
from models import Order,Sale,Shipment
from django.views.generic.list import ListView
from django.core.exceptions import ValidationError

from django.views.generic import DetailView,  UpdateView, DeleteView
from proyecto.views.crear_order import Formulario_alta_Order
from django.core.urlresolvers import reverse,reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.ofcorators import login_required
from proyecto.messages.models import Message
from proyecto.almacen.models import Product
from django.contrib import messages
from django_fsm_log.models import StateLog
from easy_pdf.views import PDFTemplateView
from datetime import date

class LoginRequiredMixin(object):
	@classmethod
	def as_view(cls,**initkwargs):
		view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
		return login_required(view)

class OrderListView(LoginRequiredMixin,ListView):
	order 		  	= Order
	template_name 	= "list_orders.html"
	paginate_by 	= 3
	def get_context_data(self, **kwargs):
    		context = super(OrderListView, self).get_context_data(**kwargs)    		
    		return context
    		
class OrdersUsuarioListView(LoginRequiredMixin,ListView):
	template_name = "list_orders2.html"
	def get_queryset(self):
		return Order.objects.filter(user = self.request.user)
	def get_context_data(self, **kwargs):
    		context = super(OrdersUsuarioListView, self).get_context_data(**kwargs)    		
    		return context	

class OrderDetailView(LoginRequiredMixin,DetailView):
	order 			   = Order
	template_name	   = "order_detail.html"
	def get_context_data(self, **kwargs):
    		context = super(OrderDetailView, self).get_context_data(**kwargs)
    		if not self.request.user.is_super:
				try:
					N = Message.objects.filter(user = self.request.user)
				except Message.DoesNotExist:
					N = ()
				try:
					H = StateLog.objects.filter(object_id=self.object.id)
				except StateLog.DoesNotExist:
		  			H=""
				try:
					E = Shipment.objects.get(order= self.object.id)
				except Shipment.DoesNotExist:
					E= ""
				context['Message']  = N #paso un sum of messages
				context['H'] = H
				context['shipment']= E
    		return context
	def get_queryset(self):
		if not self.request.user.is_super: 
			return Order.objects.filter(user = self.request.user)
		else:
			return Order.objects.all()
    		

class OrderUpdateView(LoginRequiredMixin,UpdateView):
	def clean(self):
    	    super(Order, self).clean()
	order 			= Order
	fields 			= ['paid','module',]
	template_name 	= "order_edit.html"
	success_url  	= reverse_lazy('panel')
	def post(self, request, *args, **kwargs):		
		if "cancel" in request.POST:
			self.object = self.get_object()
			url = self.get_success_url()
			return HttpResponseRedirect(url)
		else:
			return super(OrderUpdateView, self).post(request, *args, **kwargs)

class OrderDeleteView(LoginRequiredMixin,DeleteView):
	"""State to cancel and get on sale available again
	"""
	order  				= Order
	template_name 		="order_confirm_oflete.html"
	success_url 		= reverse_lazy('panel')
	def post(self, request, *args, **kwargs):
		if "cancel" in request.POST:
			self.object = self.get_object()
			url = self.get_success_url()
			return HttpResponseRedirect(url)
		else:
			self.object = self.get_object()
			self.object.estado='ca'
			self.object.save()
			m = Product.objects.get(pk=self.object.module.id)
			m.on_sale=True
			m.save()
			messages.warning(request, 'Order marked as cancelado <b>correctly</b>.')
			#NOtificar
			return HttpResponseRedirect(reverse_lazy('index'))


class SaleListView(LoginRequiredMixin,ListView):
	"""View for admin for all sales
	"""
	order 		  	= Sale
	template_name 	= "sales_list.html"
	paginate_by 	= 5
	# def get_queryset(self):
	# 	return Sale.objects.all()
	def get_context_data(self, **kwargs):
    		context = super(SaleListView, self).get_context_data(**kwargs)    		
    		return context
    		
class SalesUsuarioListView(LoginRequiredMixin,ListView):
	"""Sales list for users
	"""
	template_name = "sales2_list.html"
	def get_queryset(self):
		return Sale.objects.filter(user = self.request.user)
	def get_context_data(self, **kwargs):
    		context = super(SalesUsuarioListView, self).get_context_data(**kwargs)    		
    		return context	

class SaleDetailView(LoginRequiredMixin,DetailView):
	"""Detail of each Sale
	"""
	order 			   = Sale
	template_name	   = "sale_detail.html"
	def get_context_data(self, **kwargs):
			context = super(SaleDetailView, self).get_context_data(**kwargs)
			order = Order.objects.get(sale= self.object)
			context['order']=order
			return context
	def get_queryset(self):
		if not self.request.user.is_super: 
			return Sale.objects.filter(pk = Order.objects.filter(user= self.request.user))
		else:
			return Sale.objects.all()

class ShipmentDetailView(LoginRequiredMixin,DetailView):
	order 			   = Shipment
	template_name	   = "shipment_detail.html"
	def get_context_data(self, **kwargs):
    		context = super(ShipmentDetailView, self).get_context_data(**kwargs)
    		return context
	def get_queryset(self):
		if not self.request.user.is_super: 
			return Shipment.objects.filter(order = Order.objects.filter(user=self.request.user))
		else:
			return Shipment.objects.all()
    		

class invoicePDF(LoginRequiredMixin,PDFTemplateView):
	"""Generator of invoices to PDF format
	"""
	template_name = "invoicePDF.html"
	def get_context_data(self, **kwargs):
		context = super(invoicePDF, self).get_context_data(**kwargs)
		try:
			u=get_object_or_404(Usuario,pk = self.request.user.id)
			context['user']=u
			ped=get_object_or_404(Order,pk =context['pk'])
			context['order']=ped
			sale=Sale.objects.get(codigo = ped.codigo_ingreso)
			context['sale']=sale
			shipment=Shipment.objects.get(order_id=ped.id)
			context['shipment']=shipment
			context['today']=date.today()
			context['pagesize']="A4",
			context['title']="INVOICE",
			pe=shipment.price_shipment
			pp = sale.price
			context['total']=pe + pp
			return context
		except ObjectDoesNotExist:
			#se imprime un pequeño error por consola
			# y los objetos relacionados a ver cual es el que ha provocado la excepción controlada
			print "ADMIN: Review errors on PDF generation - ERROR"
			return context

        # return super(invoicePDF, self).get_context_data(
        #     pagesize="A4",
        #     title="Factura",
        #     ped=Order.objects.filter(user = self.request.user),
        #     sale=Sale.objects.get(codigo = ped.codigo_ingreso),
        #     shipment=Shipment.objects.select_related('order').get(id=ped.id),
        #     hoy=datetime.date.today(),
        #     **kwargs
        # )