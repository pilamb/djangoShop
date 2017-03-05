# -*- coding: utf-8 -*-

from django.contrib import admin
from models import User_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        order = User_model
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        order = User_model
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'surname', 'name','is_admin','subscribed','is_active','sign_date',)
    list_filter = ('is_admin','is_active',)
    fieldsets = ( 
        (None, {'fields': ('email', 'password')}),
        ('personal information', {'fields': ('name','surname','second_address')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','name','surname','subscribed')}
        ),
    )
    search_fields = ('email',)
    ordering = ('sign_date',)
    filter_horizontal = ()

admin.site.register(User_model,CustomUserAdmin)
admin.site.unregister(Group)