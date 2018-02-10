# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from captcha.fields import CaptchaField

from shop.models import Order
from warehouse.models import Product
from contact_messages.models import ContactMessage


class NewConcreteOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)
            super(NewConcreteOrderForm, self).__init__(*args, **kwargs)

    required_css_class = "required"
    error_css_class = "notified-danger"
    #  TODO: captcha removed for testing
    #  captcha = CaptchaField()
    text = forms.CharField(
        max_length=1000,
        required=False,
        label="Notification",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write here an optional message',
                'onblur': 'this.placeholder="Write here an optional message"',
                'onclick': 'this.placeholder=""',
                'rows': '10',
                'overflow-y': 'hidden',
                'resize': 'none'
            }
        )
    )

    class Meta:
        order = Order
        fields = ('user', 'information', 'paid',)

    def clean(self):
        cleaned_data = super(NewConcreteOrderForm, self).clean()
        return cleaned_data


def page(request, pk):
    try:
        mod = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        raise Product.DoesNotExist
    user = request.user
    if request.POST:
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            form = NewConcreteOrderForm(request.POST)
            if request.user.is_authenticated():
                if form.is_valid():
                    p = Order(
                        user=user,
                        module=mod,
                        information=mod.information,
                        paid=False,
                        )
                    if mod.on_sale:
                        mod.on_sale = False
                        mod.save()
                    p.painting = False
                    # TODO: remove all paint color logic from template view etc
                    p.save()
                    new_message = ContactMessage(
                        user=user,
                        notified=False,
                        text=u"""Congratulations, the order has been created \
                        correctly and it is in the state %s. \
                        Soon you will receive confirmation \
                        of the states changes. Thanks""" % p.state)
                    new_message.save()
                    mod.quitar_of_sale()
                    mod.save()
                    messages.success(
                        request,
                        '¡Order created <b>correctly</b>, thanks!')
                    return HttpResponseRedirect(reverse_lazy('panel'))
                else:
                    return render(request,
                                  'shop/create_order.html',
                                  {'form': form, 'pk': pk})
    else:
        form = NewConcreteOrderForm()
        return render(request, 'shop/create_order.html',
                      {'form': form, 'pk': pk})
