# -*- coding: utf-8 -*-

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy


def page(request):
    if request.POST:
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            if request.user.is_authenticated():
                return render(request, 'index.html', {'user': request.user, })
            else:
                pass 
    else:
        messages.info(request,
                      'Its mandatory communicate that this site uses '
                      '<b>cookies</b>.')
        return render(request, 'index.html')
