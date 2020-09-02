from django.contrib import admin

from accounts.client_age_filter import ClientAgeListFilter
from .models import Profile, NextOfKin


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid', 'phone', 'slug', 'updated')
    list_display_links = ('user',)
    list_filter = ('user', 'uuid', 'phone', 'timestamp', ClientAgeListFilter)
    readonly_fields = ('slug', 'image_tag')
    search_fields = ('uuid', 'user')

    ordering = ('-timestamp',)
    fieldsets = (
        ('Basic Information', {'description': "Copy User UUID",
                               'fields': ('image_tag', 'uuid', 'phone', 'image', ('user',))}),
        ('Complete Full Information', {'classes': ('collapse',), 'fields': ('bio', ('gender', 'birthday'))}),)


admin.site.site_header = 'THE VIBES VIRTUAL CLINIC'


@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'relationship', 'bio', 'phone', 'street', 'city', 'state', 'timestamp',
        'updated')
    list_display_links = ('user', 'first_name', 'phone',)
    list_filter = ('user', 'first_name', 'last_name', 'relationship', 'phone', 'street', 'city',)
    readonly_fields = ('address_tag',)
    search_fields = ('user', 'first_name', 'last_name', 'phone', 'city')

    ordering = ('-timestamp',)
