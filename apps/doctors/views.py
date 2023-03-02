import calendar
from datetime import datetime
from datetime import date
from datetime import timedelta
from http import HTTPStatus

from dateutil.relativedelta import relativedelta
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from .models import Doctor, Pago
from .forms import DoctorForms, PayForms, UpdateCMVPForms, PagoForms
from ..core.models import Sale, PayMethod


# Create your views here.

class DoctorView(ListView):
    # model = Doctor
    template_name = 'doctors/list_doctors.html'
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        kword = self.request.GET.get('kword', )

        if kword:
            return Doctor.object.listar_doctores_kword(kword)
        return Doctor.object.listar_doctores()


class DoctorCreate(SuccessMessageMixin, CreateView):
    model = Doctor
    form_class = DoctorForms
    template_name = 'doctors/add_doctor.html'

    success_message = "Médico registrado correctamente"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'FICHA ÚNICA DE INSCRIPCIÓN'
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DoctorUpdate(SuccessMessageMixin, UpdateView):
    model = Doctor
    form_class = DoctorForms
    template_name = 'doctors/add_doctor.html'

    # success_url = reverse_lazy('list_doctors')
    success_message = "Datos Actualizados correctamente"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'ACTUALIZACIÓN DE DATOS PERSONALES'
        return context


class DoctorDetail(DetailView):
    model = Doctor
    template_name = 'doctors/detail_doctor.html'

    # context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['book_list'] = .objects.all()
        return context


def get_active(fecha):
    hoy = date.today()
    activo = date.fromisoformat(str(fecha))

    start_date = date(year=hoy.year, month=hoy.month, day=1)

    if start_date <= activo:
        return True
    return False


VENTA = 'V'
COMPRA = 'C'


def pay_doctor(request):
    if request.method == "POST":
        num_cuotas = str(request.POST.get('num_cuotas', ''))
        monto = str(request.POST.get('monto', ''))
        pk = int(request.POST.get('pk', ''))

        metodo_pago_id = int(request.POST.get('pago',''))
        metodo_pago_obj = PayMethod.objects.get(id=metodo_pago_id)


        sale_obj = Sale(
            tipo=VENTA,
            estado=True,
            es_cuota=True,
            metodo_pago=metodo_pago_obj,
        )
        sale_obj.total_sale = int(num_cuotas) * float(monto)
        sale_obj.save()

        metodo_pago_obj.quantity_venta += 1
        metodo_pago_obj.total_venta = float(metodo_pago_obj.total_venta) + sale_obj.total_sale
        metodo_pago_obj.save()

        pago = Pago(
            num_cuotas=num_cuotas,
            monto=monto,
            sale=sale_obj
        )
        pago.save()

        doctor = Doctor.object.get(pk=pk)
        doctor.pagos.add(pago)
        doctor.save()

        if doctor.fecha_pagado:
            doctor.fecha_pagado += relativedelta(months=int(num_cuotas))
            doctor.fecha_activo = doctor.fecha_pagado + relativedelta(months=2)

        doctor.fecha_ultimo_pago = date.today()
        doctor.es_activo = get_active(doctor.fecha_activo)
        doctor.save()

        return JsonResponse({
            'success': True,
            'pk': pk,
            'monto': monto,
            'num_cuotas': num_cuotas,
            'message': 'Pago Registrado correctamente',
        }, status=HTTPStatus.OK)


class DoctorPayUpdate(SuccessMessageMixin, UpdateView):
    model = Doctor
    form_class = PayForms
    template_name = 'doctors/pay_quota.html'

    success_url = reverse_lazy('list_doctors')
    success_message = "Pago Registrado Correctamente"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        metodos_pago = PayMethod.objects.all()
        context['metodos_pago'] = metodos_pago

        return context
    """
    def get(self, request, *args, **kwargs):
        num_cuotas = self.request.GET.get('num_cuotas', )
        monto = self.request.GET.get('monto', )

        if num_cuotas and monto:
            pago = Pago(num_cuotas=num_cuotas, monto=monto)
            pago.save()
            self.object.pagos.add(pago)

            if self.object.fecha_pagado:
                self.object.fecha_pagado += relativedelta(months=int(num_cuotas))
                self.object.fecha_activo = self.object.fecha_pagado + relativedelta(months=2)

            self.object.fecha_ultimo_pago = date.today()
            self.object.es_activo = get_active(self.object.fecha_activo)
            self.object.save()
            url = f'/doctors/print_ticket_old/{self.object.pk}'
            url2 = f'/doctors/detail_doctor/{self.object.pk}'

            return redirect(url2)

        #else:
            #messages.error(request, "Ingresar Numero de Cuotas y/o Precio de Cuota")

        return super().get(request, *args, **kwargs)

    
    def post(self, request, *args, **kwargs):
        fecha_post = request.POST['fecha_mes']

        if not fecha_post:
            url = f'/doctors/detail_doctor/{self.object.pk}/pay_quota/'
            messages.error(request, "Ingresar Fecha")
            return redirect(url)

        fecha_post = f"{fecha_post}-01"

        f1 = date.fromisoformat(fecha_post)

        if self.object.fecha_pagado:
            f2 = self.object.fecha_pagado

            if f1 <= f2:
                messages.error(request,
                               "FECHA INCORRECTA, Ingrese una fecha posterior al pago realizado el mes anterior")
                url = f'/doctors/detail_doctor/{self.object.pk}/pay_quota/'
                return redirect(url)

        self.object.fecha_pagado = f1
        self.object.fecha_activo = f1 + relativedelta(months=2)
        self.object.es_activo = get_active(self.object.fecha_activo)
        self.object.fecha_ultimo_pago = date.today()

        self.object.save()
        messages.success(request, "Pago Registrado Correctamente")
        url = f'/doctors/detail_doctor/{self.object.pk}'
        return redirect(url)

        # return super().post(request, *args, **kwargs)
"""


class DoctorCMVPUpdate(SuccessMessageMixin, UpdateView):
    model = Doctor
    form_class = UpdateCMVPForms
    template_name = 'doctors/update_CMVP.html'

    # success_url = reverse_lazy('list_doctors')
    success_message = "Datos Actualizados correctamente"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        fecha_emision = request.POST['fecha_emision']
        fecha_mes = request.POST['fecha_mes']

        if fecha_emision:
            self.object.fecha_caducidad = datetime.strptime(fecha_emision, "%Y-%m-%d").date() + relativedelta(
                years=5) - timedelta(days=1)
            self.object.save()

        if fecha_mes:
            fecha_pagado = f'{fecha_mes}'

            f1 = date.fromisoformat(fecha_pagado)
            self.object.fecha_pagado = f1
            self.object.fecha_activo = f1 + relativedelta(months=2)
            self.object.es_activo = get_active(self.object.fecha_activo)

            self.object.save()

        # messages.success(request, "Pago Registrado Correctamente")
        url = f'/doctors/detail_doctor/{self.object.pk}'
        # return redirect(url)
        return super().post(request, *args, **kwargs)
