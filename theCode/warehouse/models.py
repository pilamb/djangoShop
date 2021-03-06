# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from theCode.core.validators import positive_price


class Piece(models.Model):
    """
    Electrical pieces which compose the main circuit of the products.
    N-M relationship.
    """

    PIECES_CHOICES = (
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

    UNITS_CHOICES = (
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
    name = models.CharField(max_length=20, blank=False, verbose_name='Name')
    quantity = models.PositiveIntegerField(default=0)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    unit = models.CharField(max_length=3, choices=UNITS_CHOICES, default='?')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    the_type = models.CharField(max_length=25, choices=PIECES_CHOICES,
                                blank=False, default='unknown')
    provider = models.URLField(blank=True)
    picture = models.ImageField(upload_to='pieces', null=True, blank=True)
    note = models.CharField(max_length=200,  default="",
                            blank=True, verbose_name=u'Additional text')
    alarm = models.BooleanField(default=False, verbose_name=u'Not available')

    def few_units(self):
        """
        notifies if units are low.
        """
        if self.quantity <= 2:
            self.alarm = True

    def __unicode__(self):
        return u'%s%s%s' % (self.name, str(self.value), self.unit)

    class Meta:
        verbose_name_plural = 'Pieces'


class Product(models.Model):
    """
    a product is composed of pieces
    """

    types = (
        ('Custom made circuitry 1', 'Custom made circuitry 1'),
        ('Delay', 'Delay'),
        ('DrumSynth8', 'SrumSynth8'),
        ('Guitar', 'Guitar'),
    )
    name = models.CharField(max_length=50,
                            unique=True, blank=False,
                            verbose_name='Name')
    sign_date = models.DateField(auto_now_add=True)
    on_sale = models.BooleanField(default=False)
    information = models.CharField(max_length=1000,blank=True,
                                   verbose_name=u'Profile')
    type_info = models.CharField(max_length=20, choices=types,
                                 blank=False,default='Custom made circuitry 1')
    picture = models.ImageField(upload_to='products',
                                null=True, blank=True)
    price = models.DecimalField(max_digits=5,
                                decimal_places=2, validators=[positive_price])
    recipe = models.ManyToManyField(Piece)
    url_sample = models.URLField(blank=True)
    #  a url showing the product or alike
    visits_number = models.PositiveIntegerField(default=0)

    def remove_from_sale(self):
        self.on_sale = False

    class Meta:
        app_label = "warehouse"
        verbose_name_plural = "Products"

    def __unicode__(self):
        return u'%s, of %s - %s €' % (
            self.name,
            self.type_info,
            str(self.price)
        )

    def get_absolute_url(self):
        return reverse('detail_product', args=[str(self.id)])
