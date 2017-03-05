# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView,  UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from datetime import date
from theCode.views.create_user2 import Form_Alta_User_model
from models import User_model
from theCode.formularios.autenticar import logout 
from theCode.shop.models import Order
from django.contrib.auth.ofcorators import login_required
from django.contrib import messages


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls,**initkwargs):
        view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
        return login_required(view)

class User_modelListView(LoginRequiredMixin,ListView):
    order               = User_model
    template_name     = "listado_users.html"
    paginate_by = 4
    def get_connotified_data(self, **kwargs):
            connotified = super(User_modelListView, self).get_connotified_data(**kwargs)
            connotified['today'] = date.today()
            return connotified
    def get_queryset(self):
        """
        Return users ordered by recent sign date  and only the latter 6 ones
        """
        return User_model.objects.exclude(is_admin=True).filter(is_superuser=False).order_by('-sign_date')#[:5]

class User_modelDetailView(LoginRequiredMixin,DetailView):
    template_name       = "detail_user.html"
    order                = User_model
    def get_connotified_data(self, **kwargs):
            connotified = super(User_modelDetailView, self).get_connotified_data(**kwargs)
            orders = Order.objects.filter(user = self.request.user)
            connotified['orders'] = orders            
            return connotified
    # def get_queryset(self):
    #         return User_model.objects.filter(email=self.request.user)

class User_modelUpdateView(LoginRequiredMixin,UpdateView):
    def clean(self):
            super(User_model, self).clean()
    order             = User_model
    fields             = ['name','surname','subscribed','address','phone']
    #exclude         = ['password','email','messages']
    template_name     = "edit_user.html"
    #form_class         = Form_Alta_User_model
    success_url      = reverse_lazy('panel')
    def post(self, request, *args, **kwargs):        
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            messages.success(request, 'Changes <b>correctly </b> saved.')
            return super(User_modelUpdateView, self).post(request, *args, **kwargs)

class User_modelDeleteView(LoginRequiredMixin,DeleteView):
    """USERS CANT BE DELETED JUST SAVED AS INACTIVE :)
    """
    order                  = User_model
    template_name         ="user_confirm_delete.html"
    success_url         = reverse_lazy('panel')
    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            u = request.user
            if u.is_superuser:
                messages.warning(request,'¡Operation not allowd over ROOT!')
                
                #los admins ni se borran ni se marcan como borrados, solo ofsof el panel
            else:
                u.is_active=False
                u.save()
                logout(request)
                messages.success(request, 'Account deleted <b>correctly</b>.')
            return HttpResponseRedirect(reverse_lazy('index'))
        
    #def get_queryset(self):
        #qs = super(User_modelDeleteView, self).get_queryset()
        #return User_model.objects.filter(email = self.request.user.email)