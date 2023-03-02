from django.contrib import admin
from .models import Doctor, Pago


# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'es_activo', 'fecha_pagado', 'fecha_activo')


admin.site.register(Doctor, DoctorAdmin)


class PagoAdmin(admin.ModelAdmin):
    list_display = ('monto', 'num_cuotas', 'fecha', 'sale')


admin.site.register(Pago, PagoAdmin)
