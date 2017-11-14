# -*- coding: utf-8 -*-

from datetime import date
from django.views.generic.list import ListView
from django.views.generic import DetailView,  UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from theCode.customForms.authenticate import logout
from shop.models import Order
from models import UserModel


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *args):
        view = super(LoginRequiredMixin, cls).as_view(*args)
        return login_required(view)


class UserModelListView(LoginRequiredMixin, ListView):
    order = UserModel
    template_name = "clients/users_list.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(UserModelListView, self).get_context_data(**kwargs)
        context['today'] = date.today()
        return context

    def get_queryset(self):
        """
        Return users ordered by recent sign date  and only the latter 5 ones
        """
        return UserModel.objects.exclude(
            is_admin=True).filter(
            is_superuser=False).order_by('-sign_date')  # [:5]


class UserModelDetailView(LoginRequiredMixin, DetailView):
    template_name = "clients/user_detail.html"
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super(UserModelDetailView, self).get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user)
        context['orders'] = orders
        return context


class UserModelUpdateView(LoginRequiredMixin, UpdateView):
    # order = UserModel
    fields = ['name', 'surname', 'subscribed', 'address', 'phone']
    # exclude       = ['password','email','messages']
    template_name = "clients/user_edit.html"
    # form_class = Form_Alta_UserModel
    success_url = reverse_lazy('panel')
    model = UserModel

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            messages.success(request, 'Changes <b>correctly </b> saved.')
            return super(UserModelUpdateView, self).\
                post(request, *args, **kwargs)

    def clean(self):
        super(UserModelUpdateView, self).clean()

    def get_queryset(self):
        super(UserModelUpdateView, self).get_queryset()
        try:
            return UserModel.objects.filter(email=self.request.user.email)
        except Exception as er:
            raise Exception(er) # TODO: improve this


class UserModelDeleteView(LoginRequiredMixin, DeleteView):
    """
    Users cant be deleted just marked as inactive
    """
    order = UserModel
    template_name = "clients/user_confirm_delete.html"
    success_url = reverse_lazy('panel')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            #  self.object = self.get_object()
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            u = request.user
            if u.is_superuser:
                messages.warning(request, '¡Operation not allowed over ROOT!')
            else:
                u.is_active = False
                u.save()
                logout(request)
                messages.success(request, 'Account deleted <b>correctly</b>.')
            return HttpResponseRedirect(reverse_lazy('index'))

    def get_queryset(self):
        super(UserModelDeleteView, self).get_queryset()
        return UserModel.objects.filter(email=self.request.user.email)
