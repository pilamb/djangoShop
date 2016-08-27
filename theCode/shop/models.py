# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from proyecto.core.validador import only_letters, alfan, nums, positive_price
from django.core.exceptions import ObjectDoesNotExist
from django_fsm import FSMField, transition
from random import randint
from datetime import date, timeoflta 
from proyecto.clients.models import Usuario
from proyecto.almacen.models import Product
from proyecto.messages.models import Message


class Sale (models.Model):
	"""
	An instance of Sale is creted when the order goes from 'waiting' to 'accepted'
	, waiting to be paid. A unique generated key is needed for the client to be able 
	to make the payment with the subject-concept as the key. 
	(payment_code 1-1 code)
	"""
	price  		= models.DecimalField(max_digits=5, ofcimal_places=2, help_notified="€", validators = [positive_price])
	sign_date 	= models.DateTimeField(auto_now_add=True)
	code 		= models.CharField(blank=True, max_length=6)  #must be the same as the code generated at the Order class

	def __unicode__(self):
		return str(self.sign_date.strftime('%Y-%m-%d %H:%M'))

	def view_sale(self):
		return '<a href="/sale/view/%s">See detail</a>' % self.id
		ver_sale.allow_tags = True


class Status(object):
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
	"""
	Contstants representing states of the Finite State Machine
		
	"""
=======
	"""
	Contstants representing states of the Finite State Machine
		
	"""
>>>>>>> more English translating
	ON_HOLD 	= u'On hold' 
	ACEPTADO 	= 'Accepted'
	REJECTED 	= 'Rejected'
	PAID 		= 'Paid'
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
	MANUFACTURE = 'Fabricación'
=======
	MANUFACTURE = 'Manufacturing'
>>>>>>> more English translating
	PAINTING 	= 'Painting'
	SHIPPED 	= 'Shipped'
	RECEIVED 	= 'Received'
	WARRANTY 	= 'Warranty'
	RETURNED 	= 'Returned'
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
	REPAIRING	= 'Reparación'
=======
	REPAIRING	= 'Repairing'
>>>>>>> more English translating
	CANCEL		= 'Canceled'
	ENDWARRANTY = u'End of warranty'

	state_choices = (
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
		(ON_HOLD,ON_HOLD),          # El user ha guardado your order, los admin lo han of accept
		(ACCEPTED,ACCEPTED),		# Algún admin acepta el order y se generan los datos para el pago
		(REJECTED,REJECTED),		# Algún admin rechaza el order (antes of fabricarse)
		(PAID,PAID),				# Cliente paga, se genera sale, se comienza fabricacion
		(MANUFACTURE,MANUFACTURE),	# El modulo se manuinvoice
		(PAINTING,PAINTING),		# Si el user ofcició pintarlo, se pinta
		(SHIPPED,SHIPPED),			# Se envia
		(RECEIVED,RECEIVED),		# El cliente lo recibe
		(WARRANTY,WARRANTY),		# Tras recibirlo, comienza la garantía
		(RETURNED,RETURNED),		# El CLIENTE en algún punto, lo ofvuelve
		(REPAIRING,REPAIRING),		# El order entra en reparación, solamente si sigue en garantía
		(CANCEL,CANCEL),			# Los ADMINS en algún punto ofl proceso, cancelan el order, "soft oflete"
		(ENDWARRANTY,ENDWARRANTY),	# Tras un año of uso, se agota la garantía
=======
		(ON_HOLD,ON_HOLD),          #  El user has made an order, admin must accept it
		(ACCEPTED,ACCEPTED),		#  Some admin accept the order, data for payment gets generated
		(REJECTED,REJECTED),		#  Some admin rejects the order (before manufacturing)
		(PAID,PAID),				#  Client pays, sale is generated, manufacturing starts
		(MANUFACTURE,MANUFACTURE),	#  the product gets manufacturing
		(PAINTING,PAINTING),		#  If user selected painting
		(SHIPPED,SHIPPED),			#  Product is sent
		(RECEIVED,RECEIVED),		#  Client confirms reception
		(WARRANTY,WARRANTY),		#  After receiving it, the warranty starts (1 year)
		(RETURNED,RETURNED),		#  Client at some point decides to return it back
		(REPAIRING,REPAIRING),		#  Order enters repairing only if it is still under warranty
		(CANCEL,CANCEL),			#  ADMINS cancel the order for some reason
		(ENDWARRANTY,ENDWARRANTY),	#  Warranty ends after a year of use
>>>>>>> more English translating
	)


class Order(models.Model):
	"""
	An order can have different states.
	"""
	COLORES_CHOICES = (
		(u'No color', u'No color (+0€)'),
		('Black', u'Black (+10€)'),
		('Pink', u'Pink (+10€)'),
		('White', u'White (+15€)'),
		('Red', u'Red (+10€)'),
		('Blue', u'Blue (+10€)'),
	)
		
	user 				= models.ForeignKey(Usuario)
	sign_date 			= models.DateField(auto_now_add=True)
	paid 				= models.BooleanField(default=False)
	payment_code 		= models.CharField(blank=True, max_length=6)
	modulo				= models.OneToOneField(Product)
	pintura 			= models.BooleanField(default=False)
	information  		= models.CharField(blank=True, max_length=1000)
	color 				= models.CharField(max_length=10, choices=COLORES_CHOICES, blank=False, default=u'No color')
	invoice_available 	= models.BooleanField(default=False)
	sale 				= models.ForeignKey(Sale, blank=True, null=True)
	icon 				= models.CharField(max_length=50, default="inbox")  # of Bootstrap class
	state				= FSMField(
	 	choices = Status.state_choices,
	 	blank = False,
	 	default = Status.ON_HOLD,
	 	protected = True,  # Only admins are allowed to change this
	 	verbose_name = 'Status of the order')

	def __unicode__(self):
		return str(self.id)
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
		# return u'ID: %s,Módulo: %s,De: %s' % (str(self.id),self.modulo.name,self.user.email)

=======
		
>>>>>>> more English translating
	class Meta:
		ordering = ("-sign_date"),

	def notify_user(self,notified):
		"""
		Creates a message to tell the user a new event
		"""
		new_notification = Message(user=self.user, notified=False, notified=notified)
		new_notification.save()
		
	def generate_payment_code(self):
		"""
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
		Genera un número aleatorio que esté entre el número of día en que se genera,
		multiplicado por mil, y en un rango of hasta mil más. Ese número lo tiene que 
		poner el cliente en el ignreso/transferencia.
=======
		Generates a random number between the current generation day and thousand the times
		, in a range of 1000 more. That number MUST be pointed by the client when the 
		money withadrawal is done. Product payment reference.
>>>>>>> more English translating
		"""
		low_range = int(date.today().day)*1000
		high_range = low_range + 1000
		secret = randint(low_range,high_range)
		return str(secret)

	#
	# States of transition 
	#

	def still_guaranteed(self):
		delivery_date = Shipment.objects.get(order_id = self.pk).date_recepcion
		return (delivery_date<= date.today() <= delivery_date+timeoflta(days=365))
	still_guaranteed.hint = '1 year counting from shipment delivered.'

	def paid_checked(self):
		return self.paid
	paid_checked.hint = 'Payment is required.'

	def painting_choosen(self):
		return True #Arreglar
		#return self.pintura
	painting_choosen.hint = 'Optional: clients choosal.'

<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
	# def disponible(self):
	# 	return self.Status == 
	# disponible.hint = 'Comprueba que...'

=======
>>>>>>> more English translating
	def shipment_delivered(self):
		if Shipment.objects.filter(order=self.pk).exists():
			return Shipment.objects.get(order=self.pk).received
		else:
			return False
	shipment_delivered.hint = "Shipment is marked as received."

	def shipment_created(self):
		return Shipment.objects.filter(order=self).exists()
	shipment_created.hint = u"Shipment need creation. Or if it is a reship, change the created one."

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
	    self.icon  ="ok"
	    self.save()
	    notified = u"Payment code is available: %s. Its mandatory point that code as concept in your payment facilities" % self.payment_code
	    self.notify_user(notified)

	@transition(field=state, source=Status.ACCEPTED,target=Status.PAID)
	def pay(self):
		"""
		Admin confirms receiving the payment.
		Notifies the user and creates a instance of sale.
		"""
		v = Sale(price=self.modulo.price,codigo=self.payment_code)
		v.save()
		self.icon  ="credit-card"
		self.paid = True
		self.save()
		notified = u"We have received your payment. Order goes to state PAID and after will go to MANUFACTURE."
 		self.notify_user(notified)

	@transition(field=state, source=Status.PAID,target=Status.MANUFACTURE,conditions=[paid_checked])
	def manufacture(self):
		"""
		The item passes to manufacture time.
		"""
		self.icon = "wrench"
		notified = "Your order has changed to manufacturing. Soon you will receive new updates. Your inbox will receive a message."
		self.notify_user(notified)
		self.save()

	@transition(field=state, source=Status.MANUFACTURE,target=Status.PAINTING,conditions=[])#painting_choosen
	def pintar(self):
		"""
		This step is optional, the user may select colour or not
		"""
		self.icon = "tint"
		notified = u"Your order is now under paintings."
		self.notify_user(notified)
		self.save()

	@transition(field=state, source=[Status.MANUFACTURE,Status.PAINTING,Status.RETURNED,Status.REPAIRING],
				 target=Status.SHIPPED,conditions=[shipment_created])
	def enviar(self):
		"""
		Generate tracking number, date of shipment, price of shipment, and notify the user.
		"""
		self.icon = "plane"
		seg = Shipment.objects.filter(order=self)
		notified = u"Your order has been shipped. Trackin number is %s" % str(seg)
		self.notify_user(notified)
		self.save()

	@transition(field=state, source=Status.SHIPPED,target=Status.RECEIVED,conditions=[shipment_delivered])
	def recibir(self):
		"""
		User received the parcel. Marck shipment as received.
		Generates the pdf invoice
		"""
		self.icon = "circle-arrow-down"
		notified = u"Your order shipment has been marked as received.."
		self.notify_user(notified)
		self.save()
		invoice_disponible = True

	@transition(field=state, source=Status.RECEIVED,target=Status.WARRANTY,conditions=[shipment_delivered])
	def comenzar_garantia(self):
		"""
		User has received the order and it has been returned.
		"""
		self.icon = "sunglasses"
		notified = u""" Thanks for trusting on us, hope you like it.
					Your 1 year warranty starts now, 
					The application will notify when a year passes"""
		self.notify_user(notified)
		self.save()

	@transition(field=state, source='*',target=Status.CANCEL,conditions=[])
	def cancelar(self):
		"""
		At any step the order gets cancel.
		"""
		notified = u"Your order has been cancel. Please contact for further info."
		self.icon ="trash"
		self.notify_user(notified)
		self.save()

	@transition(field=state, source=Status.SHIPPED,target=Status.RETURNED,conditions=[])
	def ofvolver_shipment(self):
		"""
		Some problem with shipment company, and it needs resending.
		"""
		notified = u"Your order is on returned state. We expect deliver it soon. Thanks."
		self.icon ="plane"
		self.notify_user(notified)
		self.save()

	@transition(field=state, source=Status.WARRANTY,target=Status.REPAIRING,conditions=[still_guaranteed])
	def reparar(self):
		"""
		Been under warranty, it enters on repair.
		"""
		self.icon ="wrench"
		notified = u"Your order has arrived to repairing. New updates soon."
		self.notify_user(notified)
		self.save()

	@transition(field=state, source=Status.WARRANTY,target=Status.ENDWARRANTY,conditions=[still_guaranteed])
	def finalizar_garantia(self):
		"""
		The warranty period has finished, notify the user.
		"""
		self.icon="hourglass"
		notified = u"The warranty period has finished."
		self.notify_user(notified)
		self.save()


class Shipment(models.Model):
	number 					= models.CharField(max_length=15, blank=False, null=False)  # Tracking number
	sign_date 				= models.DateField(auto_now=True)
	date_recepcion			= models.DateField(auto_now=False, auto_now_add=False, null=True)
	shipment_price 			= models.DecimalField(max_digits=5, ofcimal_places=2, help_notified="€", validators=[positive_price])
	additional_info 		= models.CharField(max_length=1000, blank=True, null=True)
	comp 					= models.CharField(max_length=20,blank=True,null=True,verbose_name='Company')  # Shipment company
	received 				= models.BooleanField(default=False)
	order 					= models.ForeignKey(Order)
<<<<<<< 9d91132817820e448c9812923042b09ec7571c60
	url_comp 				= models.URLField(null=True)  # dirección of la página of seguimiento ofl paquete
=======
	url_comp 				= models.URLField(null=True)  # address for tracking parcel
>>>>>>> more English translating

	def __unicode__(self):
		return self.number

	class Meta:
		ordering = ("-sign_date"),

	@property
	def get_shipment_price(self):
		return self.shipment_price
