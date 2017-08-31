# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from captcha.fields import CaptchaField
from django.forms import RadioSelect
from django.contrib import messages
from django.contrib.auth.models import User

from notifications.models import Notification
from theCode.core.validators import only_letters, nums
from clients.models import UserModel


class NewUserModel(forms.Form):

    required_css_class = "required"
    error_css_class = "notified-danger"
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write an email',
                'onblur': 'this.placeholder="Write an email"',
                'onclick': 'this.placeholder=""',
                'type': 'email'
            }
        )
    )
    password = forms.CharField(
        max_length=9,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose a password',
                'onblur': 'this.placeholder="Choose a password"',
                'onclick': 'this.placeholder=""',
                'type': 'password'
            }
        )
    )
    password2 = forms.CharField(
        max_length=9,
        required=False,
        label="Repeat",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Repeat the password',
                'onblur': 'this.placeholder="Repeat the password"',
                'onclick': 'this.placeholder=""',
                'type': 'password'
            }
        )
    )
    name = forms.CharField(
        max_length=20,
        label="Name",
        validators=[only_letters],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write a name of contact',
                'onblur': 'this.placeholder="Write a name of contact"',
                'onclick': 'this.placeholder=""'
            }
        )
    )
    surname = forms.CharField(
        max_length=40,
        label="Surname",
        validators=[only_letters],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write your surname',
                'onblur': 'this.placeholder="Write your surname"',
                'onclick': 'this.placeholder=""'
            }
        )
    )
    phone = forms.CharField(
        max_length=9,
        required=False,
        label="Phone",
        validators=[nums],
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone',
                'onblur': 'this.placeholder="A Phone"',
                'onclick': 'this.placeholder=""',
            }
        )
    )
    captcha = CaptchaField()
    subscribed = forms.BooleanField(
        label="subscribed",
        required=False
    )
    i_accept = forms.BooleanField(label="Accept")

    def clean_email(self):
        import ipdb
        email = self.cleaned_data.get('email').lower()
        ipdb.set_trace()
        return email

    def clean_password2(self):
        pas = self.cleaned_data.get('password', '')
        pas2 = self.cleaned_data.get('password2', '')
        if not pas2 or not pas:
            raise forms.ValidationError("You must enter a password.")
        elif pas != pas2:
            raise forms.ValidationError("Passwords must match.")
        return pas

    def clean_i_accept(self):
        terms_check = self.cleaned_data.get('i_accept')
        if not terms_check:
            raise forms.ValidationError(
                "It is mandatory to accept the conditions.")
        return terms_check


def page(request):
    if request.POST:
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            form = NewUserModel(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                email = form.cleaned_data['email']  # TODO: all email on upper
                pas2 = form.cleaned_data['password2']
                tel = form.cleaned_data['phone']
                new_user = UserModel(
                    email=email.lower(),
                    is_active=True,
                    name=name,
                    surname=surname,
                    phone=tel,
                    messages=1)
                new_user.set_password(pas2)
                # TODO: play with commit False. If captcha fails creates user
                # anyways.
                new_user.save()
                new_notification = Notification(
                    user=new_user,
                    notified=False,
                    text=u"""Welcome to the website!
                         You have an available account.""")
                new_notification.save()
                messages.success(request, 'New user created correctly.')
                # TODO: authenticate user otherwise next will always go to index
                if request.user.is_anonymous:
                    return HttpResponseRedirect(reverse_lazy('index'))
                else:
                    if request.user.is_admin:
                        return HttpResponseRedirect(reverse_lazy('users_list'))
                    else:
                        return HttpResponseRedirect(reverse_lazy('panel'))
            else:
                return render(request, 'clients/user_create.html', {'form': form})
    else:
        form = NewUserModel()
        return render(request, 'clients/user_create.html', {'form': form})
