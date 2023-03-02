import datetime

from django.db import models
from django.db.models import Q


class SaleManager(models.Manager):
    def sales_list(self):
        result = self.all()
        return result

    def list_between_dates_and_type(self, tipo, fecha1, fecha2):
        date1 = datetime.datetime.strptime(fecha1, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(fecha2, "%Y-%m-%d").date()

        result = self.filter(
            fecha_venta__range=(date1, date2),
            tipo=tipo
        )

        return result

    def list_between_dates(self, fecha1, fecha2):
        date1 = datetime.datetime.strptime(fecha1, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(fecha2, "%Y-%m-%d").date()

        result = self.filter(
            fecha_venta__range=(date1, date2)
        )

        return result

    def list_type(self, tipo):
        result = self.filter(
            tipo=tipo
        )

        return result
