from django.contrib import admin
from .models import Certificate, Lot


# Register your models here.


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'precio')


admin.site.register(Certificate, CertificateAdmin)


class LotAdmin(admin.ModelAdmin):
    list_display = ('certificate', 'stock', 'correlative_start', 'correlative_end', 'correlative_now')


admin.site.register(Lot, LotAdmin)
