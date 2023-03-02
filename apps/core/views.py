import decimal
import json
from http import HTTPStatus

from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .models import Sale, SaleDetail, BuyDetail, DetailLot, PayMethod
from ..doctors.models import Doctor, Pago
from ..certificates.models import Certificate, Lot


# Create your views here.

def buy_form(request):
    context = {}

    certificados = Certificate.objects.all()
    context['certificados'] = certificados

    metodos_pago = PayMethod.objects.all()
    context['metodos_pago'] = metodos_pago

    return render(request, 'core/add_buy.html', context)


COMPRA = 'C'
VENTA = 'V'


@csrf_exempt
def save_buy(request):
    if request.method == 'GET':
        buy_request = request.GET.get('buy', '')
        data_buy = json.loads(buy_request)

        date = str(data_buy["Date"])
        metodo_pago_id = str(data_buy["Pago"])
        metodo_pago_obj = PayMethod.objects.get(id=metodo_pago_id)

        sale_obj = Sale(
            tipo=COMPRA,
            fecha_venta=date,
            estado=True,
            metodo_pago=metodo_pago_obj,

        )
        sale_obj.save()

        for detail in data_buy['Details']:
            # recuperamos del producto
            certificate_id = int(detail['Certificate'])
            certificate_obj = Certificate.objects.get(id=certificate_id)

            quantity = int(detail['Quantity'])
            price = decimal.Decimal(detail['Price'])

            num_inicial = int(detail['Numeracion_I'])
            num_final = int(detail['Numeracion_F'])

            lote = Lot(
                certificate=certificate_obj,
                stock=quantity,
                correlative_start=num_inicial,
                correlative_end=num_final,
                correlative_now=num_inicial,
            )
            lote.save()

            certificate_obj.stock += quantity
            certificate_obj.save()

            new_buy_detail = {
                'sale': sale_obj,
                'certificate': certificate_obj,
                'quantity': quantity,
                'price_unit': price,
                'lot': lote
            }
            new_buy_detail_obj = BuyDetail.objects.create(**new_buy_detail)
            new_buy_detail_obj.save()

        response = 0
        buy_detail_set = BuyDetail.objects.filter(sale__id=sale_obj.id)
        for pd in buy_detail_set:
            response = response + (pd.quantity * pd.price_unit)
        sale_obj.total_sale = response
        sale_obj.save()

        metodo_pago_obj.quantity_compra += 1
        metodo_pago_obj.total_compra += response
        metodo_pago_obj.tipo = COMPRA
        metodo_pago_obj.save()

        return JsonResponse({
            'message': 'VENTA REGISTRADA CORRECTAMENTE.',

        }, status=HTTPStatus.OK)


def sale_form(request):
    context = {}

    certificados = Certificate.objects.all()
    context['certificados'] = certificados

    doctores = Doctor.object.listar_doctores()
    context['doctores'] = doctores

    metodos_pago = PayMethod.objects.all()
    context['metodos_pago'] = metodos_pago

    return render(request, 'core/add_sale.html', context)


@csrf_exempt
def save_sale(request):
    if request.method == 'GET':
        sale_request = request.GET.get('sale')
        # print(purchase_request)
        data_sale = json.loads(sale_request)

        doctor_id = str(data_sale["Doctor"])
        date = str(data_sale["Date"])
        metodo_pago_id = str(data_sale["Pago"])
        metodo_pago_obj = PayMethod.objects.get(id=metodo_pago_id)

        doctor_obj = Doctor.object.get_doctor(id=doctor_id)

        sale_obj = Sale(
            tipo=VENTA,
            fecha_venta=date,
            estado=True,
            metodo_pago=metodo_pago_obj,
        )
        sale_obj.save()

        for detail in data_sale['Details']:
            quantity = int(detail['Quantity'])
            price = decimal.Decimal(detail['Price'])
            # recuperamos del producto
            certificate_id = int(detail['Certificate'])
            certificate_obj = Certificate.objects.get(id=certificate_id)

            if certificate_obj.stock < quantity:
                messages.error(request, "Cantidad superada al Stock disponible")
                return redirect('add_sale')

            certificate_obj.stock -= quantity
            certificate_obj.save()

            new_sale_detail = {
                'sale': sale_obj,
                'certificate': certificate_obj,
                'quantity': quantity,
                'price_unit': price,
            }
            new_sale_detail_obj = SaleDetail.objects.create(**new_sale_detail)

            lotes = Lot.objects.filter(certificate_id=certificate_id, stock__gt=0)

            for lote in lotes:
                if lote.stock >= quantity:
                    print("Un lote")
                    lote.stock -= quantity
                    count = lote.correlative_now + quantity - 1
                    detail_lot = DetailLot(start=lote.correlative_now, end=count, quantity=quantity)
                    detail_lot.save()
                    lote.correlative_now = count + 1
                    new_sale_detail_obj.list_lots.add(detail_lot)
                    # lista_lotes.append({'lote': lote, 'quantity': quantity})
                    lote.save()
                    break
                else:
                    print("menos de un lote")
                    quantity -= lote.stock
                    detail_lot = DetailLot(start=lote.correlative_now, end=lote.correlative_end, quantity=quantity)
                    detail_lot.save()
                    new_sale_detail_obj.list_lots.add(detail_lot)
                    # lista_lotes.append({'lote': lote, 'quantity': lote.stock})
                    lote.stock = 0
                    lote.save()

            new_sale_detail_obj.save()

        pago = Pago(num_cuotas=None, monto=None, sale=sale_obj)
        pago.save()
        doctor_obj.pagos.add(pago)
        doctor_obj.save()

        ###
        response = 0
        sale_detail_set = SaleDetail.objects.filter(sale__id=sale_obj.id)
        for pd in sale_detail_set:
            response = response + (pd.quantity * pd.price_unit)
        sale_obj.total_sale = response
        sale_obj.save()

        metodo_pago_obj.quantity_venta += 1
        metodo_pago_obj.total_venta += response
        metodo_pago_obj.save()
        ###

        return JsonResponse({
            'message': 'VENTA REGISTRADA CORRECTAMENTE.',
        }, status=HTTPStatus.OK)


class DetailView(ListView):
    # model = Pago
    template_name = 'core/detail.html'
    # context_object_name = 'sales'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tipo
        tipo = self.request.GET.get("tipo", "")
        # Fecha 1
        f1 = self.request.GET.get("fecha1", "")
        # Fecha 2
        f2 = self.request.GET.get("fecha2", "")

        total = 0

        if tipo and f1 and f2:
            sales = Sale.objects.list_between_dates_and_type(tipo, f1, f2)
        elif f1 and f2:
            sales = Sale.objects.list_between_dates(f1, f2)
        elif tipo:
            sales = Sale.objects.list_type(tipo)
        else:
            sales = Sale.objects.sales_list()

        for i in sales:
            total += i.total_sale

        context['sales'] = sales
        context['total'] = total

        return context

    def get_queryset(self):
        return Sale.objects.sales_list()


class CartView(DetailView):
    model = Sale
    template_name = 'core/cart_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        buy = Sale.objects.list_type(COMPRA)
        total_buy = 0
        for i in buy:
            total_buy += i.total_sale

        context['buy'] = total_buy

        sale = Sale.objects.list_type(VENTA)
        total_sale = 0
        for i in sale:
            total_sale += i.total_sale

        context['sale'] = total_sale

        cert_vac = BuyDetail.objects.filter(certificate_id=1)
        cant_buy_vac = 0
        cant_total_buy_vac = 0
        for i in cert_vac:
            cant_buy_vac += i.quantity
            cant_total_buy_vac += i.multiplicate()
        context['cant_buy_vac'] = cant_buy_vac
        context['cant_total_buy_vac'] = cant_total_buy_vac

        cert_salud = BuyDetail.objects.filter(certificate_id=2)
        cant_buy_salud = 0
        cant_total_buy_salud = 0
        for i in cert_salud:
            cant_buy_salud += i.quantity
            cant_total_buy_salud += i.multiplicate()
        context['cant_buy_salud'] = cant_buy_salud
        context['cant_total_buy_salud'] = cant_total_buy_salud

        cert_int = BuyDetail.objects.filter(certificate_id=3)
        cant_buy_int = 0
        cant_total_buy_int = 0
        for i in cert_int:
            cant_buy_int += i.quantity
            cant_total_buy_int += i.multiplicate()
        context['cant_buy_int'] = cant_buy_int
        context['cant_total_buy_int'] = cant_total_buy_int

        cert_hab = BuyDetail.objects.filter(certificate_id=4)
        cant_buy_hab = 0
        cant_total_buy_hab = 0
        for i in cert_hab:
            cant_buy_hab += i.quantity
            cant_total_buy_hab += i.multiplicate()
        context['cant_buy_hab'] = cant_buy_hab
        context['cant_total_buy_hab'] = cant_total_buy_hab

        ######################################################

        cert_vac = SaleDetail.objects.filter(certificate_id=1)
        cant_sale_vac = 0
        cant_total_sale_vac = 0
        for i in cert_vac:
            cant_sale_vac += i.quantity
            cant_total_sale_vac += i.multiplicate()
        context['cant_sale_vac'] = cant_sale_vac
        context['cant_total_sale_vac'] = cant_total_sale_vac

        cert_salud = SaleDetail.objects.filter(certificate_id=2)
        cant_sale_salud = 0
        cant_total_sale_salud = 0
        for i in cert_salud:
            cant_sale_salud += i.quantity
            cant_total_sale_salud += i.multiplicate()
        context['cant_sale_salud'] = cant_sale_salud
        context['cant_total_sale_salud'] = cant_total_sale_salud

        cert_int = SaleDetail.objects.filter(certificate_id=3)
        cant_sale_int = 0
        cant_total_sale_int = 0
        for i in cert_int:
            cant_sale_int += i.quantity
            cant_total_sale_int += i.multiplicate()
        context['cant_sale_int'] = cant_sale_int
        context['cant_total_sale_int'] = cant_total_sale_int

        cert_hab = SaleDetail.objects.filter(certificate_id=4)
        cant_sale_hab = 0
        cant_total_sale_hab = 0
        for i in cert_hab:
            cant_sale_hab += i.quantity
            cant_total_sale_hab += i.multiplicate()
        context['cant_sale_hab'] = cant_sale_hab
        context['cant_total_sale_hab'] = cant_total_sale_hab

        pagos = Pago.objects.payment_list()
        cant_pagos = 0
        total_pagos = 0
        for i in pagos:
            if i.num_cuotas:
                cant_pagos += i.num_cuotas
                total_pagos += i.total()

        context['cant_pagos'] = cant_pagos
        context['total_pagos'] = total_pagos

        context['metodos_pago'] = PayMethod.objects.all()

        return context


def carrito(request):
    context = {}



    return render(request, 'core/carrito.html', context)