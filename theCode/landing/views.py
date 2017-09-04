# -*- coding: utf-8 -*-
from django.shortcuts import render


def help_view(request):
    return render(request, 'landing/help.html')


def cookies_view(request):
    return render(request, 'landing/cookies.html')


def about_view(request):
    return render(request, 'landing/about.html')