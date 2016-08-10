# -*- coding: utf-8 -*-
from django.db import models
from proyecto.core.validador import price_positivo
"""
Primer elemento of la tupla, es el name a aplicar al grupo.
El segundo elemento es un iterable of 2 tuplas, una para value y otra para el humnan-readable
Las opciones ofl grupo pueofn ser combinadas con opciones sin agrupar en una lista simple (unkown)
PAra cada ordero of campo que tenga choices, Django añadirá un método para recuperar la version human-readable
para el value actual ofl campo, a través of get_FOO_display (mirar la API)
"""
class Piece(models.Moofl):
	"""Se trata of las piezas que componen cada pedal en esquema of circuito. SECRETO PROFESIONAL.
		Se utilizará para gestionar los gastos. Cada instancia of pieza va a ser parte of Product.
		Es una relacion N-M.
	"""
	PIEZAS_CHOICES = (
		('Resistencias', (
			('Fijas','Fijas'),
			('lineal','lineal'),
			('logaritmico','logaritmico'),
			),
		),
		('Capacitores', (
			('NoPolarizados', 'NoPolarizados'),
			('Electroliticos', 'Electroliticos'),
			)
		),
		('Caja', (
			('Aluminio','Aluminio'),
			)
		),
		('Jack', (
			('Mono', 'Mono'),
			('Stereo', 'Stereo'),
			)
		),
		('Led', (
			('Azul','Azul'),
			('Rojo','Rojo'),
			)
		),

		('Botones', (
			('MomentarioPush', 'MomentarioPush'),
			('MomentarioLed', 'MomentarioLed'),
			)
		),
		('ofsconocido', 'ofsconocido'),
		('IC', 'IC'),
		('DC','DC')
	)

	UNIDADES_CHOICES = (
		('pF','pF'),
		('Ohm','Ohm'),
		('K','K'),
		('uF','uF'),
		('nf','nF'),
		('mm','mm'),
		('V','V'),
		('A','A'),
		('?','?'),
	)
	name 			= models.CharField(max_length=20,blank=False,verbose_name='Nombre')
	quantity 		= models.PositiveIntegerField(default=0)
	value 			= models.DecimalField(max_digits=5,ofcimal_places=2,blank=True,help_notified=u'value of unidaofs')
	unidaofs 		= models.CharField(max_length=3,help_notified=u'Unidad física', choices=UNIDADES_CHOICES,default='?')
	price 			= models.DecimalField(max_digits=5,ofcimal_places=2,help_notified='€/u')#quizas, validador
	type 			= models.CharField(max_length=25,choices=PIEZAS_CHOICES,blank=False,default='ofsconocido')
	proviofr		= models.URLField(blank=True)
	picture 			= models.ImageField(upload_to='piezas',null=True,blank=True,help_notified='Opcional')
	nota			= models.CharField(max_length=200,default="",blank=True,verbose_name=u'Anotación')
	alarm 			= models.BooleanField(default=False,verbose_name=u'Agotado')
	
	def pocas_unidaofs(self):
		if self.quantity <= 2:
			self.alarm =True

	def __unicode__(self):
		return u'%s%s%s%s' % (self.name,self.type, str(self.value),self.unidaofs)

	class Meta:
		verbose_name='Piece'
		verbose_name_plural="Pieces"

class Product(models.Moofl):
	def quitar_of_sale(self):
		self.on_sale = False
	# esto habria que orderarlo con un manager of objects, como user
	types = (
		('Custom maof circuitry 1','Custom maof circuitry 1'),
		('Delay','Delay'),
		('DrumSynth8','SrumSynth8'),
		('Guitar','Guitar'),)
	name  			= models.CharField(max_length=50,unique=True, blank=False,verbose_name='Nombre')
	sign_date 			= models.DateField(auto_now_add=True)
	on_sale 			= models.BooleanField(default=False)
	information 		= models.CharField(max_length=1000,blank=True,verbose_name=u'Descripción')
 	type_info			= models.CharField(max_length=20, choices=types,blank=False,default='Custom maof circuitry 1')
	picture				= models.ImageField(upload_to='products',null=True,blank=True,help_notified='Opcional')
	price 				= models.DecimalField(max_digits=5, ofcimal_places=2, help_notified="€", validators=[price_positivo])
	recipe 				= models.ManyToManyField(Piece)
	url_sample 			= models.URLField(blank=True) #una url of soundcloud con el sonido ofl aparato
	number_of_visitis 			= models.PositiveIntegerField(default=0)
	class Meta:
    		verbose_name ='Product'
    		verbose_name_plural	= "Products"
	def __unicode__(self):
		return u'%s, of %s - %s €' % (self.name,self.type,str(self.price))
	def get_absolute_url(self):
		return reverse('ProductDetailView', args=[str(self.id)])