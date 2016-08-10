# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from proyecto.core.validador import letras,alfan,nums,price_positivo
from django.core.exceptions import ObjectDoesNotExist
from django_fsm import FSMField, transition
from random import randint
from datetime import date, timeoflta 
from proyecto.clients.models import Usuario
from proyecto.almacen.models import Product
from proyecto.messages.models import Message

class Sale (models.Moofl):
	"""Se crea una instancia of sale cuando el order pasa of 'En espera' a 'Aceptado' y se paga
		Se necesita una clave generada única y reconocible por el sistema para que cuando el cliente
		haga el ingreso ponga esa referencia en el concepto ofl ingreso/transferencia
	"""
	#order 			= models.OneToOneField(Order)
	price  		= models.DecimalField(max_digits=5, ofcimal_places=2, help_notified="€", validators=[price_positivo])
	sign_date 		= models.DateTimeField(auto_now_add=True)
	codigo 			= models.CharField(blank=True,max_length=6)#tiene que ser exactamente igual al codigo generado ofsof Order, 1a1

	def __unicode__(self):
		return str(self.sign_date.strftime('%Y-%m-%d %H:%M'))

	def ver_sale(self):
		return '<a href="/sale/ver/%s">Ver</a>' %self.id
		ver_sale.allow_tags = True

class Estado(object):
	"""contstantes representando estados of la máquina of estados finita
		por los que pasa un order durante your ciclo of vida
	"""
	ESPERA 		= 'En espera' 
	ACEPTADO 	= 'Aceptado'
	RECHAZADO 	= 'Rechazado'
	PAGADO 		= 'Pagado'
	FABRICACION = u'Fabricación'
	PINTURA 	= 'Pintura'
	ENVIADO 	= 'Enviado'
	RECIBIDO 	= 'Received'
	GARANTIA 	= u'En Warranty'
	DEVUELTO 	= 'Devuelto'
	REPARACION	= u'Reparación'
	CANCELADO	= 'Cancelado'
	FGARANTIA 	= u'Fin of garantía'

	estado_choices = (
		(ESPERA,ESPERA),          	#El user ha guardado your order, los admin lo han of aceptar
		(ACEPTADO,ACEPTADO),		#Algún admin acepta el order y se generan los datos para el pago
		(RECHAZADO,RECHAZADO),		#Algún admin rechaza el order (antes of fabricarse)
		(PAGADO,PAGADO),			#Cliente paga, se genera sale, se comienza fabricacion
		(FABRICACION,FABRICACION),	#El modulo se manuinvoice
		(PINTURA,PINTURA),			#Si el user ofcició pintarlo, se pinta
		(ENVIADO,ENVIADO),			#Se envia
		(RECIBIDO,RECIBIDO),		#El cliente lo recibe
		(GARANTIA,GARANTIA),		#Tras recibirlo, comienza la garantía
		(DEVUELTO,DEVUELTO),		#El CLIENTE en algún punto, lo ofvuelve
		(REPARACION,REPARACION),	#El order entra en reparación, solamente si sigue en garantía
		(CANCELADO,CANCELADO),		#Los ADMINS en algún punto ofl proceso, cancelan el order, "soft oflete"
		(FGARANTIA,FGARANTIA),		#Tras un año of uso, se agota la garantía
	)

class Order(models.Moofl):
	COLORES_CHOICES = (
		('Sin',u'Sin Color (+0€)'),
		('Negro',u'Negro (+10€)'),
		('Rosa',u'Rosa (+10€)'),
		('Blanco',u'Blanco (+15€)'),
		('Rojo',u'Rojo (+10€)'),
		('Azul',u'Azul (+10€)'),
	)
		
	user 			= models.ForeignKey(Usuario)
	sign_date 			= models.DateField(auto_now_add=True)
	paid 				= models.BooleanField(default=False)
	codigo_ingreso 		= models.CharField(blank=True,max_length=6)
	modulo				= models.OneToOneField(Product)
	pintura 			= models.BooleanField(default=False)#Acabar esta parte
	information  		= models.CharField(blank=True, max_length=1000)
	#shipment 				= models.OneToOneField(Shipment,null=True)#Seguro??????
	color 				= models.CharField(max_length=10,choices=COLORES_CHOICES,blank=False,default='Sin')
	invoice_disponible 	= models.BooleanField(default=False)
	sale 				= models.ForeignKey(Sale, blank=True,null=True)
	estado				= FSMField(
	 	choices=Estado.estado_choices,
	 	blank=False,
	 	default=Estado.ESPERA,
	 	protected=True,#Así se protege la integridad of las  transiciones solo pudiendo cambiarlas ofsof admin
	 	verbose_name='Estado ofl order')
	icono 				= models.CharField(max_length=50,default="inbox")#final of la string of class en Bootstrap
	def __unicode__(self):
		return str(self.id)
		#return u'ID: %s,Módulo: %s,De: %s' % (str(self.id),self.modulo.name,self.user.email)
	class Meta:
		ordering = ("-sign_date"),

	def notificar_user(self,notified):
		notificacion_nueva = Message(user=self.user,notified=False,notified=notified)
		notificacion_nueva.save()
		
	def generar_clave_pago(self):
		"""Genera un número aleatorio que esté entre el número of día en que se genera,
		 multiplicado por mil, y en un rango of hasta mil más. Ese número lo tiene que 
		 poner el cliente en el ignreso/transferencia.
		 """
		rango_inferior = int(date.today().day)*1000
		rango_superior = rango_inferior + 1000
		secreto = randint(rango_inferior,rango_superior)
		return str(secreto) #Es único¿??
	#
	# CONDICIONES DE TRANSICIONES
	#
	def aun_garantia(self):
		date_entrega = Shipment.objects.get(order_id = self.pk).date_recepcion
		return (date_entrega<= date.today() <= date_entrega+timeoflta(days=365))
	aun_garantia.hint = 'La garantía dura un año ofsof la date of recepción.'

	def esta_paid(self):
		return self.paid
	esta_paid.hint = 'Se requiere el pago para pasar al estado of Pagado.'

	def quiere_pintura(self):
		return True #Arreglar
		#return self.pintura
	quiere_pintura.hint = 'Opcional: si el cliente eligió pintura.'

	# def disponible(self):
	# 	return self.Estado == 
	# disponible.hint = 'Comprueba que...'

	def ha_received(self):
		if Shipment.objects.filter(order=self.pk).exists():
			return Shipment.objects.get(order=self.pk).received
		else:
			return False
	ha_received.hint = "El envío ha of marcarse como received."

	def shipment_creado(self):
		return Shipment.objects.filter(order=self).exists()
	shipment_creado.hint = u"Hay que crear el shipment. O bien modificar el existente, si se trata of un reenvío."

	#
	#  TRANSICIONES DE ESTADOS 
	#

	@transition(field=estado, source=Estado.ESPERA, target=Estado.ACEPTADO)
	def aceptar(self):
	    """
	    Algún administrador acepta el order
	    Generar datos para el pago. Clave única para poner en el asunto ofl ingreso ofsof paypal.
	    Notificar al user
	    """
	    self.codigo_ingreso = self.generar_clave_pago()
	    self.icono  ="ok"
	    self.save()
	    notified = u"Ya tiene disponible el código of ingreso: %s. Es obligatorio señalar dicho código en el concepto of la transferencia (paypal) " % self.codigo_ingreso
	    self.notificar_user(notified)

	@transition(field=estado, source=Estado.ACEPTADO,target=Estado.PAGADO)
	def pagar(self):
		"""
		Se confirma la recepcion ofl order con la clave anterior, se proceof a la fabricacion
		Notificar al user y crear instancia of sale!
		"""
		v = Sale(price=self.modulo.price,codigo=self.codigo_ingreso)
		v.save()
		self.icono  ="credit-card"
		self.paid = True
		self.save()
		notified = u"Ya hemos received your ingreso. El order pasa a estado PAGADO y pronto cambiará a Fabricación."
 		self.notificar_user(notified)

	@transition(field=estado, source=Estado.PAGADO,target=Estado.FABRICACION,conditions=[esta_paid])
	def fabricar(self):
		"""
		El equipo fabrica el módulo
		"""
		self.icono ="wrench"
		notified="Tu order ha entrado en fase of fabricación. En breves recibirás nuevas actualizaciones."
		self.notificar_user(notified)
		self.save()

	@transition(field=estado, source=Estado.FABRICACION,target=Estado.PINTURA,conditions=[])#quiere_pintura
	def pintar(self):
		"""
		Esto es completamente opcional, FALTA meter el price extra en el form of creacion of order
		"""
		self.icono = "tint"
		notified = u"Su order se encuentra ahora en pintura."
		self.notificar_user(notified)
		self.save()

	@transition(field=estado, source=[Estado.FABRICACION,Estado.PINTURA,Estado.DEVUELTO,Estado.REPARACION], target=Estado.ENVIADO,conditions=[shipment_creado])
	def enviar(self):
		"""Generar Nº of seguimiento, date of shipment, price shipment->Objeto new?
		"""
		#self.shipment = Shipment(number,sign_date,price_shipment,information_adicional) Solo comprobar que existe
		self.icono = "plane"
		seg = Shipment.objects.filter(order=self)
		notified = u"Su order ha sido enviado. El número of seguimiento es %s" % str(seg)
		self.notificar_user(notified)
		#self.co
		self.save()

	@transition(field=estado, source=Estado.ENVIADO,target=Estado.RECIBIDO,conditions=[ha_received])
	def recibir(self):
		"""El user ha received el order. Marcar shipment como received
		"""
		self.icono = "circle-arrow-down"
		notified = u"Su order ha sido marcado como received."
		self.notificar_user(notified)
		self.save()
		invoice_disponible = True #sumar price shipment a price of sale

	@transition(field=estado, source=Estado.RECIBIDO,target=Estado.GARANTIA,conditions=[ha_received])
	def comenzar_garantia(self):
		"""El user ha received el order y por algún motivo nos lo envia ofvuelto
		"""
		self.icono = "sunglasses"
		notified = u"Mucha gracias por confiar en nosotros, esperamos que lo disfrutes. ¡Comienza el año of garantía!. La aplicación informará cuando pase un año."
		self.notificar_user(notified)
		self.save()

	@transition(field=estado, source='*',target=Estado.CANCELADO,conditions=[])
	def cancelar(self):
		"""En algún paso se ha cancelado el order, dar motivo
		"""
		notified = u"Su order ha sido marcado como cancelado."
		self.icono ="trash"
		self.notificar_user(notified)
		self.save()

	@transition(field=estado, source=Estado.ENVIADO,target=Estado.DEVUELTO,conditions=[])
	def ofvolver_shipment(self):
		"""Ha habido algun error en el correo y se vuelve a reenviar
		"""
		notified = u"Su order pasa al estado ofvuelto. Ha habido un error en el envío pronto informaremos con más actualizaciones."
		self.icono ="plane"
		self.notificar_user(notified)
		self.save()

	@transition(field=estado, source=Estado.GARANTIA,target=Estado.REPARACION,conditions=[aun_garantia])
	def reparar(self):
		"""Estando aún en garantía, el user hace uso of ello por algun error
		"""
		self.icono ="wrench"
		notified = u"Su order ha entrado en reparación, en breves recibirá más novedaofs."
		self.notificar_user(notified)
		self.save()

	@transition(field=estado, source=Estado.GARANTIA,target=Estado.FGARANTIA,conditions=[aun_garantia])
	def finalizar_garantia(self):
		"""El periodo of garantía ha expirado
		"""
		self.icono="hourglass"
		notified = u"El periodo of garantía of your order ha caducado."
		self.notificar_user(notified)
		self.save()
	# @transition(field=estado, source='',target='',conditions=[])
	# def verbo_al_estado(self):
class Shipment(models.Moofl):
	number 					= models.CharField(max_length=15, blank=False, null=False)#para el seguimiento
	sign_date 				= models.DateField(auto_now=True)
	date_recepcion			= models.DateField(auto_now=False, auto_now_add=False, null=True)
	price_shipment 			= models.DecimalField(max_digits=5, ofcimal_places=2, help_notified="€", validators=[price_positivo])
	information_adicional 	= models.CharField(max_length=1000,blank=True, null=True)
	comp 					= models.CharField(max_length=20,blank=True,null=True,verbose_name='Compañía')#compañía que realiza el envío
	received 				= models.BooleanField(default=False)
	order 					= models.ForeignKey(Order)
	url_comp 				= models.URLField(null=True)#dirección of la página of seguimiento ofl paquete
	def __unicode__(self):
		return self.number

	class Meta:
		ordering = ("-sign_date"),
	@property
	def get_price_shipment(self):
		return ofcimal.Decimal(self.price_shipment)
