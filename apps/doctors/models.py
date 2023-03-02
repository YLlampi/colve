from django.db import models
from django.urls import reverse

from .managers import DoctorManager, PagoManager

# Create your models here.
from ..core.models import Sale

MONTH = (
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
    "Diciembre"
)


def current_date_format(date):
    day = date.day
    month = MONTH[date.month - 1]
    year = date.year
    messsage = f'{day} de {month}, {year}'

    return messsage


def current_date_format_month(date):
    month = MONTH[date.month - 1]
    year = date.year
    message = f'{month} - {year}'
    return message


class Pago(models.Model):
    monto = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    num_cuotas = models.PositiveSmallIntegerField(null=True)
    fecha = models.DateField(auto_now=True)

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_pago', null=True)

    objects = PagoManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.num_cuotas} / {self.monto}'

    def total(self):
        return self.monto * self.num_cuotas

    def get_fecha(self):
        return f'{self.fecha.day} de {MONTH[self.fecha.month-1]}, {self.fecha.year}'


class Doctor(models.Model):
    SOLTERO = 'S'
    CASADO = 'C'
    VIUDO = 'V'
    DIVORCIADO = 'D'

    ESTADO_CIVIL_CHOICES = [
        (SOLTERO, 'Soltero'),
        (CASADO, 'Casado'),
        (VIUDO, 'Viudo'),
        (DIVORCIADO, 'Divorciado'),
    ]

    # departamento = models.CharField('CMV Departamental', max_length=50)
    # fecha = models.DateField('Fecha')
    dni = models.CharField('DNI', max_length=8, null=True, unique=True)
    # nacionalidad = models.CharField('Nacionalidad', max_length=50)
    nombres = models.CharField('Nombres', max_length=50)
    apellidos = models.CharField('Apellidos', max_length=50)
    # foto = models.ImageField('Imagen', upload_to='foto/%Y/%m/%d/', blank=True)
    # fecha_nacimiento = models.DateField('Fecha de Nacimiento')
    # nacimiento_distrito = models.CharField('Distrito', max_length=50)
    # nacimiento_provincia = models.CharField('Provincia', max_length=50)
    # nacimiento_departamento = models.CharField('Departamento', max_length=50)
    # estado_civil = models.CharField('Estado Civil', max_length=2, choices=ESTADO_CIVIL_CHOICES, default=SOLTERO)
    # nombre_conyuge = models.CharField('Nombre del Cónyuge', max_length=100, blank=True, null=True)
    # num_hijos = models.PositiveSmallIntegerField('Número de Hijos', blank=True, null=True)
    # direccion_actual = models.CharField('Dirección Actual', max_length=100)
    # direccion_distrito = models.CharField('Distrito', max_length=100)
    # direccion_provincia = models.CharField('Provincia', max_length=100)
    # direccion_departamento = models.CharField('Departamento', max_length=100)
    # telefono_fijo = models.CharField('Telefono Fijo', max_length=12, blank=True, null=True)
    # celular = models.CharField('Celular', max_length=9)
    # operador = models.CharField('Operador Movil', max_length=20)
    # email_uno = models.EmailField('Correo Electronico(1)')
    # email_dos = models.EmailField('Correo Electronico(2)', blank=True, null=True)
    # universidad_procedencia = models.CharField('Universidad de Procedencia', max_length=50)
    # fecha_egreso_bachiller = models.DateField('Fecha de Egreso(Bachiller)')
    # fecha_obtencion_titulo = models.DateField('Fehca de Obtencion(Título)')
    # especialidad_postgrado = models.CharField('Especialidad', max_length=50)
    # area_ejercicio = models.CharField('Area de Ejercicio Profesional', max_length=100)
    # centro_laboral = models.CharField('Centro Laboral', max_length=100)
    # direccion_trabajo = models.CharField('Direccion de Centro Laboral', max_length=100)
    # telefono_trabajo = models.CharField('Telefono de Centro Laboral', max_length=12, blank=True, null=True)
    # MV_voluntario = models.BooleanField('MV voluntario', default=False)

    num_CMVP = models.CharField(max_length=4, blank=True, null=True, unique=True)
    fecha_registro = models.DateField('Fecha de Registro', blank=True, null=True)

    fecha_emision = models.DateField('Fecha de Emision', blank=True, null=True)
    fecha_caducidad = models.DateField('Fecha de Caducidad', blank=True, null=True)

    es_activo = models.BooleanField('¿Médico activo?', default=False)

    fecha_mes = models.DateField('Mes Pagado', null=True, blank=True)
    fecha_pagado = models.DateField('Pagado Hasta', null=True, blank=True)
    fecha_activo = models.DateField('Activo Hasta', null=True, blank=True)

    fecha_ultimo_pago = models.DateField('Fecha Ultimo Pago', null=True, blank=True)

    pagos = models.ManyToManyField(Pago, related_name='pago_doctor')

    object = DoctorManager()

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('detail_doctor', args=[self.id])

    def get_full_name(self):
        message = f'{self.nombres} {self.apellidos}'
        return message

    def get_foto_url(self):
        # if self.foto:
        #    return self.foto.url
        # else:
        return '/static/assets/img/avatar-df.png/'

    def get_num_CMVP(self):
        if self.num_CMVP:
            return self.num_CMVP
        return f'Sin Registro'

    def get_fecha_registro(self):
        if self.fecha_registro:
            return current_date_format(self.fecha_registro)
        return f'Sin Registro'

    def get_fecha_emision(self):
        if self.fecha_emision:
            return current_date_format(self.fecha_emision)
        return f'Sin Registro'

    def get_fecha_caducidad(self):
        if self.fecha_caducidad:
            return current_date_format(self.fecha_caducidad)
        return f'Sin Registro'

    def get_fecha_activo(self):
        if self.fecha_activo:
            return current_date_format(self.fecha_activo)
        return f'Sin Registro'

    def get_fecha_activo_mes(self):
        if self.fecha_activo:
            return current_date_format_month(self.fecha_activo)
        return f'Sin Registro'

    def get_fecha_pagado(self):
        if self.fecha_pagado:
            return current_date_format(self.fecha_pagado)
        return f'Sin Registro'

    def get_fecha_pagado_mes(self):
        if self.fecha_pagado:
            return current_date_format_month(self.fecha_pagado)
        return f'Sin Registro'

    def get_fecha_ultimo_pago(self):
        if self.fecha_ultimo_pago:
            return current_date_format(self.fecha_ultimo_pago)
        return f'Sin Registro'

    def get_es_activo(self):
        if self.es_activo:
            return f'SI'
        return f'NO'

    def __str__(self):
        message = f'{self.id} - {self.nombres} {self.apellidos}'
        return message
