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
	template_name 	= "listado_orders.html"
	paginate_by 	= 3
	def get_connotified_data(self, **kwargs):
    		connotified = super(OrderListView, self).get_connotified_data(**kwargs)    		
    		return connotified
    		
class OrdersUsuarioListView(LoginRequiredMixin,ListView):
	template_name = "listado_orders2.html"
	def get_queryset(self):
		return Order.objects.filter(user = self.request.user)
	def get_connotified_data(self, **kwargs):
    		connotified = super(OrdersUsuarioListView, self).get_connotified_data(**kwargs)    		
    		return connotified	

class OrderDetailView(LoginRequiredMixin,DetailView):
	order 			   = Order
	template_name	   = "oftail_order.html"
	def get_connotified_data(self, **kwargs):
    		connotified = super(OrderDetailView, self).get_connotified_data(**kwargs)
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
				connotified['Message']  = N #paso un sum of messages
				connotified['H'] = H
				connotified['shipment']= E
    		return connotified
	def get_queryset(self):
		if not self.request.user.is_super: 
			return Order.objects.filter(user = self.request.user)
		else:
			return Order.objects.all()
    		

class OrderUpdateView(LoginRequiredMixin,UpdateView):
	def clean(self):
    	    super(Order, self).clean()
	order 			= Order
	fields 			= ['paid','modulo',]
	template_name 	= "editar_order.html"
	success_url  	= reverse_lazy('panel')
	def post(self, request, *args, **kwargs):		
		if "cancel" in request.POST:
			self.object = self.get_object()
			url = self.get_success_url()
			return HttpResponseRedirect(url)
		else:
			return super(OrderUpdateView, self).post(request, *args, **kwargs)

class OrderDeleteView(LoginRequiredMixin,DeleteView):
	"""El estado pasa a cancelado y se pone el módulo en sale
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
			m = Product.objects.get(pk=self.object.modulo.id)
			m.on_sale=True
			m.save()
			messages.warning(request, 'Order marcado como cancelado <b>correctly</b>.')
			#NOtificar
			return HttpResponseRedirect(reverse_lazy('index'))


class SaleListView(LoginRequiredMixin,ListView):
	"""Vista para el admin of todas las sales
	"""
	order 		  	= Sale
	template_name 	= "listado_sales.html"
	paginate_by 	= 5
	# def get_queryset(self):
	# 	return Sale.objects.all()
	def get_connotified_data(self, **kwargs):
    		connotified = super(SaleListView, self).get_connotified_data(**kwargs)    		
    		return connotified
    		
class SalesUsuarioListView(LoginRequiredMixin,ListView):
	"""Vista of listado para users
	"""
	template_name = "listado_sales2.html"
	def get_queryset(self):
		return Sale.objects.filter(user = self.request.user)
	def get_connotified_data(self, **kwargs):
    		connotified = super(SalesUsuarioListView, self).get_connotified_data(**kwargs)    		
    		return connotified	

class SaleDetailView(LoginRequiredMixin,DetailView):
	"""Vista en oftail of cada sale
	"""
	order 			   = Sale
	template_name	   = "oftail_sale.html"
	def get_connotified_data(self, **kwargs):
			connotified = super(SaleDetailView, self).get_connotified_data(**kwargs)
			order = Order.objects.get(sale= self.object)
			connotified['order']=order
			return connotified
	def get_queryset(self):
		if not self.request.user.is_super: 
			return Sale.objects.filter(pk = Order.objects.filter(user= self.request.user))
		else:
			return Sale.objects.all()

class ShipmentDetailView(LoginRequiredMixin,DetailView):
	order 			   = Shipment
	template_name	   = "oftail_shipment.html"
	def get_connotified_data(self, **kwargs):
    		connotified = super(ShipmentDetailView, self).get_connotified_data(**kwargs)
    		#if not self.request.user.is_super: 
    			#connotified['order'] = Order.objects.filter(pk=self.object.order.id)
    			#no es necesario, shipment ya tiene campo order
    		return connotified
	def get_queryset(self):
		if not self.request.user.is_super: 
			return Shipment.objects.filter(order = Order.objects.filter(user=self.request.user))
		else:
			return Shipment.objects.all()
    		

class invoicePDF(LoginRequiredMixin,PDFTemplateView):
	"""Generador of invoices a formato pdf con los datos pasados a connotified
	"""
	template_name = "invoicePDF.html"
	def get_connotified_data(self, **kwargs):
		connotified = super(invoicePDF, self).get_connotified_data(**kwargs)
		try:
			u=get_object_or_404(Usuario,pk = self.request.user.id)
			connotified['user']=u
			ped=get_object_or_404(Order,pk =connotified['pk'])
			connotified['order']=ped
			sale=Sale.objects.get(codigo = ped.codigo_ingreso)
			connotified['sale']=sale
			shipment=Shipment.objects.get(order_id=ped.id)
			connotified['shipment']=shipment
			connotified['hoy']=date.today()
			connotified['pagesize']="A4",
			connotified['title']="Factura",
			pe=shipment.price_shipment
			pp = sale.price
			connotified['total']=pe + pp
			return connotified
		except ObjectDoesNotExist:
			#se imprime un pequeño error por consola
			# y los objetos relacionados a ver cual es el que ha provocado la excepción controlada
			print "ADMIN: ¡¡Revisar error en la generación of invoices!! - ERROR"
			return connotified

        # return super(invoicePDF, self).get_connotified_data(
        #     pagesize="A4",
        #     title="Factura",
        #     ped=Order.objects.filter(user = self.request.user),
        #     sale=Sale.objects.get(codigo = ped.codigo_ingreso),
        #     shipment=Shipment.objects.select_related('order').get(id=ped.id),
        #     hoy=datetime.date.today(),
        #     **kwargs
        # )