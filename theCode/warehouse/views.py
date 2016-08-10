# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.oftail import DetailView
from proyecto.almacen.models import Product

class ProductsListView(ListView):
	order 	= Product
	template_name 	= "products.html"
	paginate_by = 3
	def get_connotified_data(self, **kwargs):
			connotified = super(ProductsListView, self).get_connotified_data(**kwargs)
			return connotified

class GutiarraListView(ListView):
	order 	= Product
	template_name 	= "product2.html"
	def get_connotified_data(self, **kwargs):
			connotified = super(GutiarraListView, self).get_connotified_data(**kwargs)
			return connotified
	def get_queryset(self):
		return Product.objects.filter(type='Guitar')

class DelayListView(ListView):
	order 	= Product
	template_name 	= "product3.html"
	def get_connotified_data(self, **kwargs):
			connotified = super(DelayListView, self).get_connotified_data(**kwargs)
			return connotified
	def get_queryset(self):
		return Product.objects.filter(type='Delay')

class ProductDetailView(DetailView):
	order = Product
	template_name = "oftail_product.html"
	def get_connotified_data(self, **kwargs):
		    connotified = super(ProductDetailView, self).get_connotified_data(**kwargs)
		    return connotified
	def get_object(self):
			object = super(ProductDetailView, self).get_object()
			#sumar visita
			object.number_of_visitis+=1
			object.save()
			return object