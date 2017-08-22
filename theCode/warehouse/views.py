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


class ProductDetailView(DetailView):
    order = Product
    template_name = "detail_product.html"

    def get_context_data(self, **kwargs):
            context = super(ProductDetailView, self).get_context_data(**kwargs)
            return context

    def get_object(self):
            object = super(ProductDetailView, self).get_object()
            # add visit + 1
            object.number_of_visitis += 1
            object.save()
            return object
