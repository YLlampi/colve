from django.contrib import admin
from .models import Sale, SaleDetail, BuyDetail, DetailLot, PayMethod


# Register your models here.


class SaleAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'estado', 'fecha_venta', 'es_cuota', 'total_sale', 'metodo_pago')


admin.site.register(Sale, SaleAdmin)


class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('sale', 'certificate', 'quantity', 'price_unit')


admin.site.register(SaleDetail, SaleDetailAdmin)


class BuyDetailAdmin(admin.ModelAdmin):
    list_display = ('sale', 'certificate', 'quantity', 'price_unit', 'lot')


admin.site.register(BuyDetail, BuyDetailAdmin)


class DetailLotAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'quantity')


admin.site.register(DetailLot, DetailLotAdmin)


class PayMethodAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'quantity_compra', 'total_compra', 'quantity_venta', 'total_venta')


admin.site.register(PayMethod, PayMethodAdmin)
