# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http     import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login as django_login, authenticate, logout as django_logout


class FormAutenticathe(forms.Form):
    """
    Main login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Write your email of access',
            'onblur': 'this.placeholder="Write your email of access"',
            'onclick': 'this.placeholder=""'
            }))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={
            'class':' form-control',
            'onclick': 'this.placeholder=""'
            }))

    class Meta:
        fields = ['email', 'password']


def login(request):
    """
    Login view
    """
    if request.method == 'POST':
        form = FormAutenticathe(data=request.POST)
        if form.is_valid():
            user = authenticate(
                email=request.POST['email'].
                    replace(" ", ""), password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return render_to_response('login.html', {'form': form, },
                                          context_instance=
                                          RequestContext(request))
    else:
        form = FormAutenticathe()
    return render_to_response(
        'login.html', {'form': form, },
        context_instance=RequestContext(request))


def logout(request):
    django_logout(request)
    messages.info(request, 'Your session has been successfully closed, bye!')
    return HttpResponseRedirect(reverse_lazy('login'))
