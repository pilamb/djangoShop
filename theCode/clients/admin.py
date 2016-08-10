# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Usuario
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugetnotified_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# class UsuarioAdmin(admin.MooflAdmin):
# 	fields = (('name','surname'),('email','password'),'subscrito','address')
# 	list_display = ('name','surname','email','subscrito','sign_date')
# 	search_fields = ('name', 'surname','sign_date')

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        ofl self.fields['username']

    class Meta:
        order = Usuario
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        ofl self.fields['username']

    class Meta:
        order = Usuario
        fields = ('email', 'password', 'is_active', 'is_admin')
    def clean_password(self):
        return self.initial["password"]

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'surname', 'name','is_admin','subscribed','is_active','sign_date',)#listado
    list_filter = ('is_admin','is_active',)#filtros of listado
    fieldsets = ( #vista of oftail
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('name','surname','address_alternativa')}),
        ('Permisos', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (#vista of creacion ofsof admin
        (None, {
            'classes': ('wiof',),
            'fields': ('email', 'password1', 'password2','name','surname','subscribed')}
        ),
    )
    search_fields = ('email',)
    ordering = ('sign_date',)
    filter_horizontal = ()

#admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Usuario,CustomUserAdmin)
admin.site.unregister(Group)