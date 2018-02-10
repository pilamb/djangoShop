# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone as tz
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib import messages
from captcha.fields import CaptchaField

from contact_messages.models import Alert, ContactMessage
# TODO: refactor this class as a whole OO style


class MailerForm(forms.Form):
    required_css_class = "required"
    error_css_class = "notified-danger"
    name = forms.CharField(
        max_length=20,
        label="Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write a name of contact',
                'onblur': 'this.placeholder="Write a name of contact"',
                'onclick': 'this.placeholder=""'
            }
        )
    )

    sender = forms.EmailField(
        label="Sender",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write your mail',
                'onblur': 'this.placeholder="Write your mail"',
                'onclick': 'this.placeholder=""',
                'type': 'email'
            }
        )
    )

    message_text = forms.CharField(
        max_length=1000,
        label="Notification",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write here your message',
            'onblur': 'this.placeholder="Write here your message"',
            'onclick': 'this.placeholder=""',
            'rows': '10',
            'overflow-y': 'hidden',
            'resize': 'none'
            }
        )
    )

    category = forms.ChoiceField(
        label="Category",
        choices=ContactMessage.CATEGORY,
        initial='6',
        widget=forms.Select(attrs={
            'class': 'form_control'
            }
        )
    )
    captcha = CaptchaField()


def confirm(request):
    """
    Sends email confirming the contact to the sender
    """
    category = request.get(u'category')
    name = request.get(u'name', '')
    email = request.get(u'sender', '')
    message = request.get(u'message_text', '')
    message += unicode(category)
    if category and message and email:
        try:
            send_mail(
                subject=settings.EMAIL_SUBJECT_PREFIX,
                message=u"""Hello, {0}
                 You have sent a question regarding {1}.
                 we will answer the fastest we can, thanks. \
                 Please do not answer to this automatic email.""" %
                        name % category,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
                )
        except BadHeaderError:
            return HttpResponse('Wrong header, please try again later.')
    else:
        return HttpResponse('Make sure all data are correct.')


def notify_admins():
    """
    A mail is sent to every mail that appears at Alert Class.
    So, the website admins and so, receive the message.
    """

    mails = Alert.objects.all()
    if len(mails) > 0:
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


def new_message(request):
    """
    new message gets saved at DDBB
    """
    category = request.get(u'category', '')
    name = request.get(u'name', '')
    email = request.get(u'sender', '')
    message = request.get(u'message_text', '')
    record_message = ContactMessage(
        message=message,
        name=name,
        category=category,
        mail=email.lower(),
        date=tz.now(),
        attended=False)
    record_message.save()


def page(request):
    if request.POST:
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            form = MailerForm(request.POST)
            if form.is_valid():
                # confirm(request.POST) This send email to user confirming
                # contact form has been wrote
                new_message(request.POST)
                # notify_admins()  # Admins gets a message
                messages.success(request,
                                 'Your message has been sent with '
                                 '<b>success</b>. '
                                 'Soon you will receive an answer. Thanks.')
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return render(request, 'contact_messages/contact.html',
                              {'form': form})
    else:
        form = MailerForm()
        return render(request, 'contact_messages/contact.html', {'form': form})
