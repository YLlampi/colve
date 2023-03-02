from django.db import models

from .managers import SaleManager
from ..certificates.models import Certificate, Lot

# from ..doctors.models import Doctor

# Create your models here.

MONTH = (
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
    "Diciembre"
)

PENDIENTE = 'P'
VENDIDO = 'V'

ESTADO_VENTA = [
    (PENDIENTE, 'Pendiente'),
    (VENDIDO, 'Vendido'),
]

COMPRA = 'C'
VENTA = 'V'

TIPO = [
    (COMPRA, 'Compra'),
    (VENTA, 'Venta'),
]


def current_date_format(date):
    day = date.day
    month = MONTH[date.month - 1]
    year = date.year
    messsage = f'{day} de {month}, {year}'

    return messsage


class PayMethod(models.Model):
    nombre = models.CharField('Método de Pago', max_length=100)
    quantity_compra = models.PositiveIntegerField('Cantidad Compra', default=0)
    quantity_venta = models.PositiveIntegerField('Cantidad Venta', default=0)
    total_compra = models.DecimalField('Total Compra', max_digits=10, decimal_places=2, default=0)
    total_venta = models.DecimalField('Total Venta', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.nombre}'


class Sale(models.Model):
    # doctor = models.ForeignKey(Doctor, related_name='doctor_sale', on_delete=models.CASCADE, null=True)
    tipo = models.CharField('Tipo', max_length=2, choices=TIPO, default=VENTA)
    estado = models.BooleanField('¿Vendido?', default=False)
    fecha_venta = models.DateField(auto_now=True, null=True)

    es_cuota = models.BooleanField('¿Quota?', default=False)
    total_sale = models.DecimalField('Precio Total', max_digits=10, decimal_places=2, default=0)

    metodo_pago = models.ForeignKey(PayMethod, on_delete=models.CASCADE)

    objects = SaleManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'

    def get_fecha_venta(self):
        return current_date_format(self.fecha_venta)

    def total(self):
        response = 0
        sale_detail_set = SaleDetail.objects.filter(sale__id=self.id)
        for pd in sale_detail_set:
            response = response + (pd.quantity * pd.price_unit)
        return response

    def total_buy(self):
        response = 0
        buy_detail_set = BuyDetail.objects.filter(sale__id=self.id)
        for pd in buy_detail_set:
            response = response + (pd.quantity * pd.price_unit)
        return response


class DetailLot(models.Model):
    start = models.PositiveIntegerField(null=True)
    end = models.PositiveIntegerField(null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.start} - {self.end} [{self.quantity}]'


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_detailSale', null=True, blank=True)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField('Cantidad vendida')
    price_unit = models.DecimalField('Precio unitario', max_digits=6, decimal_places=2, default=0)

    list_lots = models.ManyToManyField(DetailLot, related_name='detailLot_detailSale')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-id']

    def multiplicate(self):
        return self.quantity * self.price_unit


class BuyDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_detailBuy', null=True, blank=True)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField('Cantidad comprada')
    price_unit = models.DecimalField('Precio unitario', max_digits=6, decimal_places=2, default=0, null=True,
                                     blank=True)
    # correlative_start = models.PositiveIntegerField(null=True)
    # correlative_end = models.PositiveIntegerField(null=True)

    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, related_name='lot_detailBuy', null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-id']

    def multiplicate(self):
        return self.quantity * self.price_unit
