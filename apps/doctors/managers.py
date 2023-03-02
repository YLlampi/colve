import datetime

from django.db import models
from django.db.models import Q

class PagoManager(models.Manager):
    def payment_list(self):
        result = self.all()
        return result


class DoctorManager(models.Manager):
    """
    managers para el model Doctor
    """

    def listar_doctores(self):
        # result = self.filter(num_CMVP__isnull=False)
        result = self.all()

        return result

    def listar_doctores_kword(self, kword):
        result = self.filter(
            Q(nombres__icontains=kword) |
            Q(apellidos__icontains=kword) |
            Q(num_CMVP__icontains=kword) |
            Q(dni__icontains=kword)
        )
        return result

    def get_doctor(self, id):
        return self.get(id=id)

    def asignar_fecha_activo(self, kword):
        fecha_actual = datetime.datetime.now()
