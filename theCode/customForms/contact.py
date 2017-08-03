# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError
from django.conf import settings
from captcha.fields import CaptchaField
from django.contrib import messages
from theCode.messages_app.models import Alert, MessageModel


class MailerForm(forms.Form):
    required_css_class      = "required"
    error_css_class      = "notified-danger"
    Name     = forms.CharField (max_length=20,
        label="Name",
        widget= forms.TextInput (attrs={
            'class':'form-control',
            'placeholder':'Write a name of contact',
            'onblur':'this.placeholder="Write a name of contact"',
            'onclick':'this.placeholder=""'
            } 
    ))

    Sender     = forms.EmailField(label="Sender",
        widget= forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Write your mail',
            'onblur':'this.placeholder="Write your mail"',
            'onclick':'this.placeholder=""',
            'type':'email'
            }
    )) 
    
    Mensj     = forms.CharField ( max_length=1000,
        label="Notification",
        widget= forms.Textarea(attrs={
            'class':'form-control',
            'placeholder':'Write here  your message',
            'onblur':'this.placeholder="Write here  your message"',
            'onclick':'this.placeholder=""',
            'rows':'10',
            'overflow-y':'hidofn',
            'resize':'none'
            } 
    ))
    
    Category = forms.ChoiceField(
        label="Category",
        choices=MessageModel.CATEGORY,
        initial='6',
        widget= forms.Select(attrs={
            'class':'form_control'
            }
    ))

    captcha = CaptchaField()


def confirmar(request):
    """
    Its confirmed that it has been sent.
    """
    category = request.get(u'Category')
    name = request.get(u'Name', '')
    email = request.get('Sender', '')
    message = request.get(u'Mensj', '')
    message += unicode(category)
    if category and message and email:
        try:
            send_mail(
                subject=settings.EMAIL_SUBJECT_PREFIX,
                 message=u"""Hello,
                 You have sent a question regarding "%s". 
                 we will answer the fastest we can, thanks. 
                 Please do not answer to this automatic email.""" % category,
                 from_email=settings.EMAIL_HOST_USER,
                 recipient_list=[email],
                 fail_silently=False
                 )
        except BadHeaderError:
            return HttpResponse('Wrong header, please try again later.')
    else:
        return HttpResponse('Make sure all data are correct.')

def avisar():
    """
    A mail is sent to every mail that appears at Alert Class.
    So, the website admins and so, receive the message.
    """

    mails = Alert.objects.all()
    for i in mails:
        try:
            send_mail(
                subject="Admin: New message",
                 message=u"""Hello,
                 A new message has been received.""",
                 from_email=settings.EMAIL_HOST_USER,
                 recipient_list=[i.email],
                 fail_silently=False
                 )
        except BadHeaderError:
            return HttpResponse('Wrong header, please try again later.')
            
def newMessage_class(request):
    """
    new message gets saved at DDBB
    """
    category = request.get(u'Category', '')
    name = request.get(u'Name', '')
    email = request.get('Sender', '')
    message = request.get(u'Mensj', '')
    print message
    grabar = MessageModel(message=message, name=name, category=category, mail=email, attended=False)
    grabar.save()

def page(request):
    if request.POST:
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            form = MailerForm(request.POST)
            if form.is_valid():
                confirmar(request.POST)
                newMessage_class(request.POST)
                avisar()  # Admins gets a message
                messages.success(request, 'Your message has been sent with <b>success</b>. Soon you will receive an answer. Thanks.')
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return render(request, 'contact2.html',{'form':form})
    else:
        form=MailerForm()
        return render(request,'contact2.html',{'form':form})
