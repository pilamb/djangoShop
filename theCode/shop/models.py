# -*- coding: utf-8 -*-

from random import randint
from datetime import date, timedelta

from django.db import models
from django_fsm import FSMField, transition

from clients.models import UserModel
from warehouse.models import Product
from contact_messages.models import ContactMessage
from theCode.core.validators import positive_price


class Sale(models.Model):
    """
    An instance of Sale is created when the order goes from 'waiting' to
    'accepted', waiting to be paid. A unique generated key is needed for
    the client to be able to make the payment with subject-concept as the key.
    (payment_code 1-1 code)
    """
    price = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                validators=[positive_price])
    sign_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(blank=True,
                            max_length=6)
    #  must be the same as the code generated at the Order class

    def __unicode__(self):
        return str(self.sign_date.strftime('%Y-%m-%d %H:%M'))

    def view_sale(self):
        # view_sale.allow_tags = True
        return '<a href="/sale/view/%s">See detail</a>' % self.id


class Status(object):
    """
    Constants representing states of the Finite State Machine
    """

    ON_HOLD = u'On hold'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    PAID = 'Paid'
    MANUFACTURE = 'Manufacturing'
    PAINTING = 'Painting'
    SHIPPED = 'Shipped'
    RECEIVED = 'Received'
    WARRANTY = 'Warranty'
    RETURNED = 'Returned'
    REPAIRING = 'Repairing'
    CANCEL = 'Canceled'
    ENDWARRANTY = u'End of warranty'
    state_choices = (

        (ON_HOLD, ON_HOLD),  # El user has made an order, admin must accept it
        (ACCEPTED, ACCEPTED),  # Some admin accept the order, data for
        # payment gets generated
        (REJECTED, REJECTED),  # Some admin rejects the order (before
        # manufacturing)
        (PAID, PAID),   # Client pays, sale is generated,
        # manufacturing starts
        (MANUFACTURE, MANUFACTURE),  # the product gets manufacturing
        (PAINTING, PAINTING),  # If user selected painting
        (SHIPPED, SHIPPED),  # Product is sent
        (RECEIVED, RECEIVED),  # Client confirms reception
        (WARRANTY, WARRANTY),  # After receiving it the warranty starts (1 year)
        (RETURNED, RETURNED),  # Client at some point decides to return it back
        (REPAIRING, REPAIRING),  # Order enters repairing only if it
        # is still under warranty
        (CANCEL, CANCEL),  # ADMINS cancel the order for some reason
        (ENDWARRANTY, ENDWARRANTY),  # Warranty ends after a year of use
    )


class Order(models.Model):
    """
    An order can have different states.
    """
    COLORS_CHOICES = (
        (u'No color', u'No color (+0€)'),
        ('Black', u'Black (+10€)'),
        ('Pink', u'Pink (+10€)'),
        ('White', u'White (+15€)'),
        ('Red', u'Red (+10€)'),
        ('Blue', u'Blue (+10€)'),
    )

    user = models.ForeignKey(UserModel, null=True)
    sign_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    payment_code = models.CharField(blank=True, max_length=6)
    module = models.OneToOneField(Product)
    # painting = models.BooleanField(default=False)
    information = models.CharField(blank=True, max_length=1000)
    # color = models.CharField(max_length=10,
    #                         choices=COLORS_CHOICES,
    #                         blank=False,
    #                         default=u'No color')
    invoice_available = models.BooleanField(default=False)
    sale = models.ForeignKey(Sale, blank=True, null=True)
    icon = models.CharField(max_length=50, default="inbox")
    state = FSMField(
         choices=Status.state_choices,
         blank=False,
         default=Status.ON_HOLD,
         protected=True,  # Only admins are allowed to change this
         verbose_name='Status of the order')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = "-sign_date",

    def notify_user(self, text):
        """
        Creates a message to tell the user a new event
        """
        new_notification = ContactMessage(user=self.user,
                                          message=text,
                                          notified=False
                                          )
        new_notification.save()

    def generate_payment_code(self):
        """
        Generates a random number between the current generation day and thousand the times
        , in a range of 1000 more. That number MUST be pointed by the client when the
        money withadrawal is done. Product payment reference.
        """
        low_range = int(date.today().day)*1000
        high_range = low_range + 1000
        secret = str(randint(low_range, high_range))
        return unicode(secret)

    #
    # States of transition 
    #

    def still_guaranteed(self):
        delivery_date = Shipment.objects.get(order_id=self.pk).date_recepcion
        return (delivery_date <= date.today() <= delivery_date+timedelta(
            days=365))
    still_guaranteed.hint = '1 year counting from shipment delivered.'

    def paid_checked(self):
        return self.paid
    paid_checked.hint = 'Payment is required.'

    def painting_choosen(self):
        return True  # TODO: fix this
        # return self.pintura
    painting_choosen.hint = 'Optional: clients choosal.'

    def shipment_delivered(self):
        if Shipment.objects.filter(order=self.pk).exists():
            return Shipment.objects.get(order=self.pk).received
        else:
            return False
    shipment_delivered.hint = "Shipment is marked as received."

    def shipment_created(self):
        return Shipment.objects.filter(order=self).exists()
    shipment_created.hint = u"Shipment need creation. " \
                            u"Or if it is a reship, change the created one."

    #
    #  Transition from states 
    #

    @transition(field=state, source=Status.ON_HOLD, target=Status.ACCEPTED)
    def accept(self):
        """
        Some Admin user must accept the order. Generate data fot the payment. A unique key code is provided.
        With that the user can use it as concept fot Paypal or so.
        Notifies the user.
        """
        self.payment_code = self.generate_payment_code()
        self.icon = "ok"
        self.save()
        text = u"Payment code is available: %s. " \
               u"Its mandatory point that code as " \
               u"concept in your payment facilities" % self.payment_code
        self.notify_user(text)

    @transition(field=state, source=Status.ACCEPTED, target=Status.PAID)
    def pay(self):
        """
        Admin confirms receiving the payment.
        Notifies the user and creates a instance of sale.
        """
        v = Sale(price=self.modulo.price,code=self.payment_code)
        v.save()
        self.icon = "credit-card"
        self.paid = True
        self.save()
        text = u"We have received your payment. " \
               u"Order goes to state PAID and after will go to MANUFACTURE."
        self.notify_user(text)

    @transition(field=state, source=Status.PAID, target=Status.MANUFACTURE,
                conditions=[paid_checked])
    def manufacture(self):
        """
        The item passes to manufacture time.
        """
        self.icon = "wrench"
        text = u"""Your order has changed to manufacturing.
                  Soon you will receive new updates.
                  Your inbox will receive a message."""
        self.notify_user(text)
        self.save()

    @transition(field=state, source=Status.MANUFACTURE,
                target=Status.PAINTING, conditions=[])  # painting_choosen
    def paint(self):
        """
        This step is optional, the user may select colour or not
        """
        self.icon = "tint"
        text = u"Your order is now under paintings."
        self.notify_user(text)
        self.save()

    @transition(field=state,
                source=[Status.MANUFACTURE,
                        Status.PAINTING,
                        Status.RETURNED,
                        Status.REPAIRING],
                target=Status.SHIPPED,
                conditions=[shipment_created])
    def send(self):
        """
        Generate tracking number, date of shipment, price of shipment,
        and notify the user.
        """
        self.icon = "plane"
        seg = Shipment.objects.filter(order=self)
        text = u"Your order has been shipped. Tracking number is %s" % str(seg)
        self.notify_user(text)
        self.save()

    @transition(field=state, source=Status.SHIPPED, target=Status.RECEIVED,
                conditions=[shipment_delivered])
    def received(self):
        """
        User received the parcel. Marck shipment as received.
        Generates the pdf invoice
        """
        self.icon = "circle-arrow-down"
        text = u"Your order shipment has been marked as received.."
        self.notify_user(text)
        self.invoice_available = True
        self.save()

    @transition(field=state, source=Status.RECEIVED, target=Status.WARRANTY,
                conditions=[shipment_delivered])
    def start_warranty(self):
        """
        User has received the order and it has been returned.
        """
        self.icon = "sunglasses"
        text = u""" Thanks for trusting on us, hope you like it.
                    Your 1 year warranty starts now,
                    The application will notify when a year passes"""
        self.notify_user(text)
        self.save()

    @transition(field=state, source='*', target=Status.CANCEL, conditions=[])
    def cancel(self):
        """
        At any step the order gets cancel.
        """
        text = u"""Your order has been cancel.
                Please contact for further info."""
        self.icon = "trash"
        self.notify_user(text)
        self.save()

    @transition(field=state, source=Status.SHIPPED,
                target=Status.RETURNED, conditions=[])
    def return_shipment(self):
        """
        Some problem with shipment company, and it needs resending.
        """
        text = u"""Your order is on returned state.
                   We expect deliver it soon. Thanks."""
        self.icon = "plane"
        self.notify_user(text)
        self.save()

    @transition(field=state, source=Status.WARRANTY, target=Status.REPAIRING,
                conditions=[still_guaranteed])
    def repair(self):
        """
        Been under warranty, it enters on repair.
        """
        self.icon = "wrench"
        text = u"Your order has arrived to repairing. New updates soon."
        self.notify_user(text)
        self.save()

    @transition(field=state, source=Status.WARRANTY,
                target=Status.ENDWARRANTY, conditions=[still_guaranteed])
    def end_warranty(self):
        """
        The warranty period has finished, notify the user.
        """
        self.icon = "hourglass"
        text = u"The warranty period has finished."
        self.notify_user(text)
        self.save()


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=15,
                                       blank=False,
                                       null=False)
    sign_date = models.DateField(auto_now=True)
    date_reception = models.DateField(auto_now=False,
                                      auto_now_add=False,
                                      null=True)
    shipment_price = models.DecimalField(max_digits=5,
                                         decimal_places=2,
                                         validators=[positive_price])
    additional_info = models.CharField(max_length=1000,
                                       blank=True,
                                       null=True)
    comp = models.CharField(max_length=20,
                            blank=True,
                            null=True,
                            verbose_name='Company')  # Shipment company
    received = models.BooleanField(default=False)
    order = models.ForeignKey(Order)
    url_comp = models.URLField(null=True)  # address for tracking parcel

    def __unicode__(self):
        return self.tracking_number

    class Meta:
        ordering = "-sign_date",

    @property
    def get_shipment_price(self):
        return self.shipment_price
