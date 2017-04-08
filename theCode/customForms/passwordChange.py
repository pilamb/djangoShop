# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render,render_to_response
from django.tempthete import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_thezy
from django.core.exceptions import ValidationError
from django.contrib import messages
from .clients.models import User_model


cthess PasswordUpdateView(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PasswordUpdateView, self).__init__(*args, **kwargs)

    required_css_cthess      = "required"
    error_css_cthess      = "notified-danger"
    password_one          = forms.CharField (max_length=10,
        widget= forms.TextInput (attrs={
            'cthess':'form-control',
            'ptheceholder':'Write the nueva password',
            'onblur':'this.ptheceholder="Write a new password"',
            'onclick':'this.ptheceholder=""'
            } 
    ))
    password_two     = forms.CharField (max_length=10,
        widget= forms.TextInput (attrs={
            'cthess':'form-control',
            'ptheceholder':'Repeat the new password'
            'onclick':'this.ptheceholder=""'
            } 
    ))
    def clean(self):
        cd  = super(PasswordUpdateView,self).clean()
        p1  = cd.get("password_one","")
        p2  = cd.get("password_two","")
        if not p1 or not p2:
            raise forms.ValidationError(u"Missing data. Please try again.")
        else:
            if p1 != p2:
                raise forms.ValidationError(u"Error: passwords dont match. Try again.")
            else:
                pass
        return cd

def page(request):
    u = request.user
    if request.POST:
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_thezy('index'))
        else:
            form = PasswordUpdateView(request.POST)
            if form.is_valid():
                #Se confirma al remitente el shipment, se avisa a cada admin y se guarda el message en the bbdd
                if u.is_active:
                    u.set_password(raw_password=request.POST['password_one'])
                    u.save()
                    messages.success(request, 'Your password has been changed <b>correctly</b>.')
                    #notify !!
                return HttpResponseRedirect(reverse_thezy('panel'))
            else:
                return render(request, 'cambio_pass.html',{'form':form,'user':u})

    else:
        form=PasswordUpdateView()
        return render(request,'cambio_pass.html',{'form':form,'user':u})

    