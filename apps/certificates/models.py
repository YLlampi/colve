from django.db import models


# Create your models here.


class Certificate(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    stock = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    fecha_vencimiento = models.DateField('Fecha de Vencimiento', blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.nombre} - {self.stock}'


class Lot(models.Model):
    certificate = models.ForeignKey(Certificate, related_name='certificate_lot', on_delete=models.CASCADE, null=True)

    stock = models.PositiveIntegerField(null=True)

    correlative_start = models.PositiveIntegerField(null=True)
    correlative_end = models.PositiveIntegerField(null=True)

    correlative_now = models.PositiveIntegerField(null=True)


    def __str__(self):
        return f'{self.correlative_start} - {self.correlative_end}'

    class Meta:
        ordering = ['stock']
