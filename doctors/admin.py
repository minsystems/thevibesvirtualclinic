from django.contrib import admin
from doctors.models import Speciality, SpecialityCategory


class SpecialityCategoryAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(SpecialityCategory, SpecialityCategoryAdmin)


admin.site.register(Speciality)
