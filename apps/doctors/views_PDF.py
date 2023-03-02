# 5.826772
# 8.26772


import decimal
import reportlab
import io
from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A5, portrait, A6, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Spacer, Image
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.rl_settings import defaultPageSize

from apps.doctors.number_to_letters import numero_a_moneda
from veterinary import settings
from .models import Doctor

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, leading=8, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=8, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='JustifySquare', alignment=TA_JUSTIFY, leading=12, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='LeftSquare', alignment=TA_LEFT, leading=12, fontName='Square', fontSize=13))
styles.add(ParagraphStyle(name='LeftSquareSmall', alignment=TA_LEFT, leading=9, fontName='Square', fontSize=10))
styles.add(ParagraphStyle(name='LeftSquareSmall2', alignment=TA_LEFT, leading=9, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='Justify-Dotcirful', alignment=TA_JUSTIFY, leading=12, fontName='Dotcirful-Regular',
                          fontSize=10))
styles.add(
    ParagraphStyle(name='Justify-Dotcirful-table', alignment=TA_JUSTIFY, leading=12, fontName='Dotcirful-Regular',
                   fontSize=7))
styles.add(ParagraphStyle(name='Justify_Bold', alignment=TA_JUSTIFY, leading=8, fontName='Square-Bold', fontSize=8))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, leading=8, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='Center4', alignment=TA_CENTER, leading=12, fontName='Square-Bold',
                          fontSize=14, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name='Center5', alignment=TA_LEFT, leading=15, fontName='ticketing.regular',
                          fontSize=12))
styles.add(
    ParagraphStyle(name='Center-Dotcirful', alignment=TA_CENTER, leading=12, fontName='Dotcirful-Regular', fontSize=10))
styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT, leading=8, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='CenterTitle', alignment=TA_CENTER, leading=8, fontName='Square-Bold', fontSize=8))
styles.add(ParagraphStyle(name='CenterTitle-Dotcirful', alignment=TA_CENTER, leading=12, fontName='Dotcirful-Regular',
                          fontSize=10))
styles.add(ParagraphStyle(name='CenterTitle2', alignment=TA_CENTER, leading=8, fontName='Square-Bold', fontSize=12))
styles.add(ParagraphStyle(name='Center_Regular', alignment=TA_CENTER, leading=8, fontName='Ticketing', fontSize=10))
styles.add(ParagraphStyle(name='Center_Bold', alignment=TA_CENTER,
                          leading=8, fontName='Square-Bold', fontSize=12, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name='ticketing.regular', alignment=TA_CENTER,
                          leading=8, fontName='ticketing.regular', fontSize=14, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name='Center2', alignment=TA_CENTER, leading=8, fontName='Ticketing', fontSize=8))
styles.add(ParagraphStyle(name='Center3', alignment=TA_JUSTIFY, leading=8, fontName='Ticketing', fontSize=6))
style = styles["Normal"]

reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + '/static/fonts')
pdfmetrics.registerFont(TTFont('Square', 'square-721-condensed-bt.ttf'))
pdfmetrics.registerFont(TTFont('Square-Bold', 'sqr721bc.ttf'))
pdfmetrics.registerFont(TTFont('Newgot', 'newgotbc.ttf'))
pdfmetrics.registerFont(TTFont('Ticketing', 'ticketing.regular.ttf'))
pdfmetrics.registerFont(TTFont('Lucida-Console', 'lucida-console.ttf'))
pdfmetrics.registerFont(TTFont('Square-Dot', 'square_dot_digital-7.ttf'))
pdfmetrics.registerFont(TTFont('Serif-Dot', 'serif_dot_digital-7.ttf'))
pdfmetrics.registerFont(TTFont('Enhanced-Dot-Digital', 'enhanced-dot-digital-7.regular.ttf'))
pdfmetrics.registerFont(TTFont('Merchant-Copy-Wide', 'MerchantCopyWide.ttf'))
pdfmetrics.registerFont(TTFont('Dot-Digital', 'dot_digital-7.ttf'))
pdfmetrics.registerFont(TTFont('Raleway-Dots-Regular', 'RalewayDotsRegular.ttf'))
pdfmetrics.registerFont(TTFont('Ordre-Depart', 'Ordre-de-Depart.ttf'))
pdfmetrics.registerFont(TTFont('Dotcirful-Regular', 'DotcirfulRegular.otf'))
pdfmetrics.registerFont(TTFont('Nationfd', 'Nationfd.ttf'))
pdfmetrics.registerFont(TTFont('Kg-Primary-Dots', 'KgPrimaryDots-Pl0E.ttf'))
pdfmetrics.registerFont(TTFont('Dot-line', 'Dotline-LA7g.ttf'))
pdfmetrics.registerFont(TTFont('Dot-line-Light', 'DotlineLight-XXeo.ttf'))
pdfmetrics.registerFont(TTFont('Jd-Lcd-Rounded', 'JdLcdRoundedRegular-vXwE.ttf'))
pdfmetrics.registerFont(TTFont('ticketing.regular', 'ticketing.regular.ttf'))
pdfmetrics.registerFont(TTFont('allerta_medium', 'allerta_medium.ttf'))
# pdfmetrics.registerFont(TTFont('Romanesque_Serif', 'Romanesque Serif.ttf'))


# LOGO = "apps/sales/static/assets/logo_mendivil.png"
MONTH = (
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE",
    "DICIEMBRE"
)


def qr_code(table):
    # generate and rescale QR
    qr_code = qr.QrCodeWidget(table)
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(
        3.5 * cm, 3.5 * cm, transform=[3.5 * cm / width, 0, 0, 3.5 * cm / height, 0, 0])
    drawing.add(qr_code)

    return drawing


def print_ticket_old(request, pk=None):  # TICKET PASSENGER OLD

    _wt = 2.83 * inch - 4 * 0.05 * inch  # termical
    tbh_business_name_address = ''
    ml = 0.0 * inch
    mr = 0.0 * inch
    ms = 0.039 * inch
    mi = 0.039 * inch
    order_obj = Doctor.object.get(pk=pk)
    passenger_name = ""
    passenger_document = ""
    client_document = ""
    client_name = ""
    client_address = ""

    passenger_set = order_obj
    passenger_name = passenger_set.get_full_name()
    passenger_document = passenger_set.num_CMVP

    tbh_business_name_address = f'COLEGIO MÉDICO VETERINARIO DEPARTAMENTAL AREQUIPA'

    # date = order_obj.pagos.fecha
    # _format_time = datetime.now().strftime("%H:%M %p")
    # _format_date = date.strftime("%d/%m/%Y")

    line = '-----------------------------------------------------'

    # I = Image(LOGO)
    # I.drawHeight = 1.95 * inch / 2.9
    # I.drawWidth = 7.4 * inch / 2.9

    style_table = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('BOTTOMPADDING', (0, 0), (-1, -1), -4),  # all columns
        # ('BACKGROUND', (1, 0), (3, 0), colors.blue),
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('ALIGNMENT', (1, 0), (1, -1), 'RIGHT'),  # second column
        ('RIGHTPADDING', (1, 0), (1, -1), 0.5),  # second column
        ('TOPPADDING', (1, 0), (1, -1), -1),  # second column
        # ('SPAN', (1, 0), (3, 0)),

    ]
    colwiths_table = [_wt * 25 / 100, _wt * 75 / 100]

    PAGO = order_obj.pagos.last()

    p0 = Paragraph(f'{PAGO.id}', styles["Left"])
    p01 = Paragraph(f'974542692', styles["Left"])
    p02 = Paragraph(f'#966239489', styles["Left"])
    p03 = Paragraph(f'cmveterinarioaqp@gmail.com', styles["Left"])
    p04 = Paragraph(f'Cmvd arequipa', styles["Left"])
    ana_c1 = Table(
        [('N° de RECIBO: ', p0)] +
        [('RPC: ', p01)] +
        [('RPM: ', p02)] +
        [('E-mail: ', p03)] +
        [('FACEBOOK: ', p04)],
        colWidths=colwiths_table)

    ana_c1.setStyle(TableStyle(style_table))

    p10 = Paragraph('Dr. ' + passenger_name.upper(), styles["Left"])
    p101 = Paragraph(passenger_document, styles["Left"])
    p102 = Paragraph(order_obj.apellidos, styles["Left"])
    p103 = Paragraph(f'{PAGO.fecha}', styles["Left"])

    colwiths_table = [_wt * 25 / 100, _wt * 75 / 100]

    ana_c2 = Table(
        [('SR(A):', p10)] +
        [('CMVP:', p101)] +
        [('DIRECCIÓN:', p102)] +
        [('FECHA:', p103)],
        colWidths=colwiths_table)
    ana_c2.setStyle(TableStyle(style_table))

    my_style_table3 = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.pink),  # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('LEFTPADDING', (0, 0), (0, -1), 0),  # first column
        ('BOTTOMPADDING', (0, 0), (-1, -1), -6),  # all columns
        ('RIGHTPADDING', (1, 0), (-1, -1), 0),  # second column
        ('ALIGNMENT', (1, 0), (-1, -1), 'RIGHT'),  # second column
        ('ALIGNMENT', (2, 0), (-1, -1), 'RIGHT'),  # second column
    ]

    colwiths_table = [_wt * 60 / 100, _wt * 20 / 100, _wt * 20 / 100]
    ana_c6 = Table(
        [('DESCRIPCIÓN', 'COSTO/U', 'TOTAL')],
        colWidths=colwiths_table)
    ana_c6.setStyle(TableStyle(my_style_table3))

    sub_total = 0
    total = 0
    igv_total = 0

    fecha_anterior = f'{order_obj.fecha_pagado}'
    f1 = date.fromisoformat(fecha_anterior) - relativedelta(months=PAGO.num_cuotas - 1)

    P0 = Paragraph(f'NUMERO DE CUOTAS: {PAGO.num_cuotas}', styles["Justify"])

    meses = ''
    for i in range(1, PAGO.num_cuotas + 1):
        f3 = date.fromisoformat(fecha_anterior) - relativedelta(months=PAGO.num_cuotas - i)
        meses += f'{MONTH[f3.month - 1]}/{f1.year} '

    meses = meses[0:len(meses) - 1]

    P_TRUCK = Paragraph(
        # f'{MONTH[f1.month - 1]}/{f1.year} - {MONTH[order_obj.fecha_pagado.month - 1]}/{order_obj.fecha_pagado.year}',
        f'{meses}',
        styles["Justify_Bold"]
    )

    base_total = 1 * 45
    base_amount = base_total / 1.1800
    igv = base_total - base_amount
    sub_total = sub_total + base_amount
    total = total + base_total
    igv_total = igv_total + igv
    ana_truck = Table([(P_TRUCK, '')], colWidths=[_wt * 35 / 100, _wt * 65 / 100])

    my_style_truck = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.pink),   # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # all columns
        ('TOPPADDING', (0, 0), (-1, -1), -3),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('RIGHTPADDING', (1, 0), (1, -1), 0.5),  # second column
        ('ALIGNMENT', (1, 0), (1, -1), 'RIGHT'),  # second column
    ]
    my_style_table4 = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.pink),   # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('LEFTPADDING', (0, 0), (0, -1), 0),  # first column
        ('RIGHTPADDING', (2, 0), (-1, -1), 0),  # THIR column
        ('ALIGNMENT', (1, 0), (-1, -1), 'CENTER'),  # second column
        ('ALIGNMENT', (1, 0), (-1, -1), 'RIGHT'),  # second column
        ('ALIGNMENT', (2, 0), (-1, -1), 'RIGHT'),  # second column
    ]

    TOTAL = PAGO.monto * PAGO.num_cuotas

    # print(f'PAGO =======> {PAGO} ======= {TOTAL}')

    ana_c7 = Table([(P0, f'S/ {PAGO.monto}', 'S/ ' + str(decimal.Decimal(round(TOTAL, 2))))],
                   colWidths=[_wt * 60 / 100, _wt * 20 / 100, _wt * 20 / 100])
    ana_c7.setStyle(TableStyle(my_style_table4))
    ana_truck.setStyle(TableStyle(my_style_truck))

    my_style_table5 = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns

        # ('GRID', (0, 0), (-1, -1), 0.5, colors.pink),   # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('BOTTOMPADDING', (0, 0), (-1, -1), -6),  # all columns
        ('RIGHTPADDING', (2, 0), (2, -1), 0),  # third column
        ('ALIGNMENT', (2, 0), (2, -1), 'RIGHT'),  # third column
        ('RIGHTPADDING', (3, 0), (3, -1), 0.3),  # four column
        ('ALIGNMENT', (3, 0), (3, -1), 'RIGHT'),  # four column
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('FONTNAME', (0, 2), (-1, 2), 'Square-Bold'),  # third row
        ('FONTSIZE', (0, 2), (-1, 2), 10),  # third row
    ]

    ana_c8 = Table(
        [('OP. NO GRAVADA', '', 'S/', str(decimal.Decimal(round(TOTAL, 2))))] +
        [('I.G.V.  (18.00)', '', 'S/', '0.00')] +
        [('TOTAL', '', 'S/', str(decimal.Decimal(round(TOTAL, 2))))],
        colWidths=[_wt * 60 / 100, _wt * 10 / 100, _wt * 10 / 100, _wt * 20 / 100]
    )
    ana_c8.setStyle(TableStyle(my_style_table5))
    footer = 'SON: ' + numero_a_moneda(TOTAL)

    my_style_table6 = [
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.blue),   # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('ALIGNMENT', (0, 0), (0, -1), 'CENTER'),  # first column
        ('SPAN', (0, 0), (1, 0)),  # first row
    ]

    # datatable = order_obj.correlative_sale

    _dictionary = []
    # _dictionary.append(I)
    _dictionary.append(Spacer(1, 5))
    _dictionary.append(Paragraph(tbh_business_name_address.replace("\n", "<br />"), styles["Center4"]))
    _dictionary.append(Spacer(-4, -4))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Paragraph('TICKET', styles["Center_Regular"]))
    _dictionary.append(Paragraph('RECIBO: ' + str(PAGO.id).zfill(6), styles["Center_Bold"]))
    _dictionary.append(Spacer(-2, -2))
    _dictionary.append(ana_c1)
    _dictionary.append(Spacer(-4, -4))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(-2, -2))
    _dictionary.append(Spacer(1, 2))
    _dictionary.append(Paragraph('DATOS DE PAGO ', styles["Center_Regular"]))
    _dictionary.append(Spacer(1, 1))
    _dictionary.append(ana_c2)
    _dictionary.append(Spacer(1, 1))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(-1, -1))
    _dictionary.append(ana_c6)
    _dictionary.append(Spacer(-1, -1))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(1, 1))
    _dictionary.append(ana_c7)
    _dictionary.append(ana_truck)
    _dictionary.append(Spacer(-7, -7))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(ana_c8)
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Paragraph(footer, styles["Center"]))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(
        Paragraph("***COMPROBANTE NO TRIBUTARIO.***".replace('***', '"'), styles["Center2"]))
    _dictionary.append(
        Paragraph("***CANJEAR POR UN DOCUMENTO VÁLIDO.***".replace('***', '"'), styles["Center2"]))
    _dictionary.append(Spacer(4, 4))
    # _dictionary.append(Paragraph("DE LAS CONDICIONES PARA EL SERVICIO DE TRANSPORTE: "
    #                             "1. EL BOLETO DE VIAJE ES PERSONAL, TRANSFERIBLE Y/O PO5TERGABLE. "
    #                             "2. EL PASAJERO SE PRESENTARÁ 30 MIN ANTES DE LA HORA DE VIAJE, DEBIENDO PRESENTAR SU BOLETO DE VIAJE Y DNI. "
    #                             "3. LOS MENORES DE EDAD VIAJAN CON SUS PADRES O EN SU DEFECTO DEBEN PRESENTAR PERMISO NOTARIAL DE SUS PADRES, MAYORES DE 5 AÑOS PAGAN SU PASAJE. "
    #                             "4. EN CASO DE ACCIDENTES EL PASAJERO VIAJA  ASEGURADO CON SOAT DE LA COMPAÑIA DE SEGUROS. "
    #                             "5. EL PASAJERO TIENE DERECHO A TRANSPORTAR 20 KILOS DE EQUIPAJE, SOLO ARTICULOS DE USO PERSONAL (NO CARGA).  EL EXCESO SERÁ ADMITIDO CUANDO LA CAPACIDAD DE LA UNIDAD LO PERMITA, PREVIO PAGO DE LA TARIFA. "
    #                             "6. LA EMPRESA NO SE RESPONSABILIZA POR FALLAS AJENAS AL MISMO SERVICIO DE TRANSPORTE (WIFI, TOMACORRIENTES, PANTALLAS, AUDIO Y OTRAS SIMILARES) PUES ESTOS SERVICIOS SON OFRECIDOS EN CALIDAD DE CORTESIA. ",
    #                             styles["Center3"]))
    # _dictionary.append(Spacer(-4, -4))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(-2, -2))
    _dictionary.append(Paragraph("¡GRACIAS POR SU PAGO!", styles["Center2"]))
    buff = io.BytesIO()

    pz_matricial = (2.57 * inch, 11.6 * inch)
    # pz_termical = (3.14961 * inch, 11.6 * inch)
    pz_termical = (2.83 * inch, 11.6 * inch)

    doc = SimpleDocTemplate(buff,
                            pagesize=pz_termical,
                            rightMargin=mr,
                            leftMargin=ml,
                            topMargin=ms,
                            bottomMargin=mi,
                            title='TICKET'
                            )
    doc.build(_dictionary)
    # doc.build(elements)
    # doc.build(Story)
    #
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="{}-{}.pdf"'.format(
    #    order_obj.nombres, order_obj.pagos.id)
    #

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="CE[{}].pdf"'.format(
        order_obj.nombres + '-' + str(PAGO.id))

    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie('bp', value=pk, expires=expires)

    response.write(buff.getvalue())

    buff.close()
    return response
