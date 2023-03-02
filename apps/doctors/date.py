from datetime import date
from datetime import timedelta
import calendar

from dateutil.relativedelta import relativedelta


def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = f'{day} de {month}, {year}'

    return messsage


hoy = date.today()

dentro_dias = current_date_format(hoy + timedelta(days=10))
dentro_mes = current_date_format(hoy + relativedelta(months=1) - timedelta(days=1))
dentro_year = current_date_format(hoy + relativedelta(years=1) - timedelta(days=1))



def get_active(fecha):
    fecha_actual = date.today()
    fecha_actual.replace(day=calendar.monthrange(fecha_actual.year, fecha_actual.month)[1])

    today = date.fromisoformat("2020-12-27")
    fecha = date.fromisoformat(f'{fecha}')

    res = fecha_actual - fecha

    if res.total_seconds() > 0:
        return True
    else:
        return False


print(get_active("2023-01-26"))