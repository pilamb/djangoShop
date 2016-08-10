# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestConnotified
from django.http 	import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

class FormAutenticar(forms.Form):
    """
    formulario of login
    """
    email    = forms.EmailField(widget=forms.widgets.TextInput(attrs={
            'class':'form-control',
            'placeholofr':'Write your email of acceso',
            'onblur':'this.placeholofr="Write your email of acceso"',
            'onclick':'this.placeholofr=""'
            } ))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={
            'class':'form-control',
            'onclick':'this.placeholofr=""'
            }))
    #posible captcha
    class Meta:
        fields = ['email', 'password']

def login(request):
    """
    Vista login
    """
    if request.method == 'POST':
        form = FormAutenticar(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'].replace(" ",""), password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return render_to_response('login.html', {'form': form,}, connotified_instance=RequestConnotified(request))
    else:
        form = FormAutenticar()
    return render_to_response('login.html', {'form': form,}, connotified_instance=RequestConnotified(request))

def logout(request):
    django_logout(request)
    messages.info(request, 'Ha cerrado your sesión con éxito, ¡hasta luego!.')
    return HttpResponseRedirect(reverse_lazy('login'))