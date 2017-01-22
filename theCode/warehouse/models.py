# -*- coding: utf-8 -*-

from django.db import models
from theCode.core.validador import positive_price

"""
First tuple element is the name to apply to the group.
Second element is an iterable consisting on 2 tuples, one for the value, the other for the
humnan-readable. The options of the group can be combined without group`to a small lits.
For every order that has choices, Django will add a method to recover the human-readable,
for the value of the field, throught get_FOO_display (look at the API).
"""


class Piece(models.Model):
	"""
	Electrical pieces which compose the main circuit of the products.
	N-M relationship.
	""" 

	PIEZAS_CHOICES = (
		('Resistors', (
			('Steady','Steady'),
			('lineal','lineal'),
			('logarythimcs','logarythimcs'),
			),
		),
		('Capacitors', (
			('NoPolarized', 'NoPolarized'),
			('Electrolitcs', 'Electrolitcs'),
			)
		),
		('Box', (
			('Aluminio','Aluminio'),
			)
		),
		('Jack', (
			('Mono', 'Mono'),
			('Stereo', 'Stereo'),
			)
		),
		('Led', (
			('Blue','Blue'),
			('Red','Red'),
			)
		),
		('Buttons', (
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
	name 			= models.CharField(max_length=20, blank=False, verbose_name='Name')
	quantity 		= models.PositiveIntegerField(default=0)
	value 			= models.DecimalField(max_digits=5,decimal_places=2,blank=True,help_notified=u'value of units')
	unit 			= models.CharField(max_length=3,help_notified=u'Unit', choices=UNIDADES_CHOICES,default='?')
	price 			= models.DecimalField(max_digits=5, decimal_places=2, help_notified='€/u')#quizas, validador
	the_type		= models.CharField(max_length=25,choices=PIEZAS_CHOICES,blank=False,default='unkown')
	procider		= models.URLField(blank=True)
	picture 		= models.ImageField(upload_to='pieces', null=True, blank=True, help_notified='Optional')
	nota			= models.CharField(max_length=200,default="", blank=True, verbose_name=u'Additional text')
	alarm 			= models.BooleanField(default=False,verbose_name=u'Not available')
	
	def few_units(self):
		"""
		noifies if units are low
		"""
		if self.quantity <= 2:
			self.alarm =True

	def __unicode__(self):
		return u'%s%s%s%s' % (self.name,self.type, str(self.value),self.units)

	class Meta:
		verbose_name = 'Piece'
		verbose_name_plural = 'Pieces'

class Product(models.Model):
	"""
	a product is composed of pieces
	"""

	name  		= models.CharField(max_length=50,unique=True, blank=False,verbose_name='Name')
	sign_date	= models.DateField(auto_now_add=True)
	on_sale 	= models.BooleanField(default=False)
	information = models.CharField(max_length=1000,blank=True,verbose_name=u'Profile')
 	type_info	= models.CharField(max_length=20, choices=types,blank=False,default='Custom made circuitry 1')
	picture		= models.ImageField(upload_to='products',null=True,blank=True,help_notified='Optional')
	price 		= models.DecimalField(max_digits=5, decimal_places=2, help_notified="€", validators=[positive_price])
	recipe 		= models.ManyToManyField(Piece)
	url_sample 	= models.URLField(blank=True) #una url of soundcloud con el sonido ofl aparato
	visits_number	= models.PositiveIntegerField(default=0)

	def remove_from_sale(self):
		self.on_sale = False

	types = (
		('Custom maof circuitry 1','Custom maof circuitry 1'),
		('Delay','Delay'),
		('DrumSynth8','SrumSynth8'),
		('Guitar','Guitar'),
	)

	class Meta:
    		verbose_name ='Product'
    		verbose_name_plural	= "Products"

	def __unicode__(self):
		return u'%s, of %s - %s €' % (self.name,self.type,str(self.price))

	def get_absolute_url(self):
		return reverse('ProductDetailView', args=[str(self.id)])
