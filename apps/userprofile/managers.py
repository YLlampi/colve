import datetime

from django.db import models


class UserProfileManager(models.Manager):

    def get_condition(self, id_doctor):

        doctor = self.get(id=id_doctor)

        pagado_month = doctor.pagado_hasta_month
        pagado_year = doctor.pagado_hasta_year

        activo_month = (doctor.activo_hasta_month)
        activo_year = doctor.activo_hasta_year

        current_date_time = datetime.datetime.now()
        date = current_date_time.date()
        actual_year = int(date.strftime("%Y"))
        actual_month = int(date.strftime("%m"))

        # print(f"Current Year -> {type(actual_month)} - {type(actual_year)}")
        # print(f"Current Year -> {type(activo_month)} - {type(activo_year)}")

        if int(actual_year) < int(activo_year):
            return 1

        if int(actual_month) <= int(activo_month):
            return 1
        else:
            return 0


#from apps.userprofile.models import *
#datas = UserProfile.objects.get_condition(2)