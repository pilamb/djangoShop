# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from warehouse.models import Product


class ProductsListView(ListView):
    order = Product
    template_name = "products.html"
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
            context = super(ProductsListView, self).get_context_data(**kwargs)
            return context

    def get_queryset(self):
        return Product.objects.all()


class GuitarListView(ListView):
    order = Product
    template_name = "product2.html"
    
    def get_context_data(self, **kwargs):
            context = super(GuitarListView, self).get_context_data(**kwargs)
            return context
            
    def get_queryset(self):
        return Product.objects.filter(type='Guitar')


class DelayListView(ListView):
    order = Product
    template_name = "product3.html"
    
    def get_context_data(self, **kwargs):
            context = super(DelayListView, self).get_context_data(**kwargs)
            return context
            
    def get_queryset(self):
        return Product.objects.filter(type='Delay')


class ProductDetailView(DetailView):
    order = Product
    template_name = "detail_product.html"

    def get_context_data(self, **kwargs):
            context = super(ProductDetailView, self).get_context_data(**kwargs)
            return context

    def get_object(self):
            object = super(ProductDetailView, self).get_object()
            #sumar visita
            object.number_of_visitis += 1
            object.save()
            return object
