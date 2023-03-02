import decimal
import reportlab
import io
from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from reportlab.lib.colors import Color
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
from ..core.models import SaleDetail

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

styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, leading=10, fontName='Square-Bold', fontSize=10,
                          textColor=colors.steelblue))
styles.add(ParagraphStyle(name='Center-fecha', alignment=TA_CENTER, leading=10, fontName='Square-Bold', fontSize=10,
                          textColor=colors.black))
styles.add(ParagraphStyle(name='Center-datos', alignment=TA_CENTER, leading=10, fontName='Square', fontSize=10,
                          textColor=colors.black))
styles.add(ParagraphStyle(name='Center-arequipa', alignment=TA_CENTER, leading=19, fontName='Square-Bold', fontSize=10,
                          textColor=colors.steelblue))
styles.add(ParagraphStyle(name='Center-titulo', alignment=TA_CENTER, leading=20, fontName='Square-Bold', fontSize=20,
                          textColor=colors.steelblue))
styles.add(ParagraphStyle(name='Center-recibo', alignment=TA_CENTER, leading=20, fontName='Square-Bold', fontSize=20,
                          textColor=colors.white))
styles.add(ParagraphStyle(name='Center-id', alignment=TA_CENTER, leading=40, fontName='Lucida-Console', fontSize=30,
                          textColor=colors.black))
styles.add(ParagraphStyle(name='Center-ng', alignment=TA_CENTER, leading=10, fontName='Square-Bold', fontSize=10,
                          textColor=colors.steelblue))
styles.add(
    ParagraphStyle(name='Left', alignment=TA_LEFT, leading=8, fontName='Square', fontSize=8, textColor=colors.black))
styles.add(ParagraphStyle(name='Left-name', alignment=TA_LEFT, leading=8, fontName='Square-Bold', fontSize=8,
                          textColor=colors.steelblue))
styles.add(ParagraphStyle(name='Left-datos', alignment=TA_LEFT, leading=10, fontName='Square-Bold', fontSize=10,
                          textColor=colors.black))

styles.add(ParagraphStyle(name='Center4', alignment=TA_CENTER, leading=12, fontName='Square-Bold',
                          fontSize=14, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name='Center5', alignment=TA_LEFT, leading=15, fontName='ticketing.regular',
                          fontSize=12))
styles.add(
    ParagraphStyle(name='Center-Dotcirful', alignment=TA_CENTER, leading=12, fontName='Dotcirful-Regular', fontSize=10))
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


LOGO = "static/assets/img/logo-vet.png"

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


ALTURA = 5.826772
BASE = 8.26772


def print_ticket_old(request, pk=None):  # TICKET PASSENGER OLD

    _wt = BASE * inch - 4 * 0.05 * inch  # termical
    tbh_business_name_address = ''
    ml = 0.0 * inch
    mr = 0.0 * inch
    ms = 0.039 * inch
    mi = 0.039 * inch

    DOCTOR = Doctor.object.get(pk=pk)
    PAGO = DOCTOR.pagos.first()
    num_cuotas = PAGO.num_cuotas

    sales = ''

    if PAGO.sale:
        SALE = PAGO.sale.id
        sales = SaleDetail.objects.filter(sale_id=SALE)

    passenger_name = ""
    passenger_document = ""
    client_document = ""
    client_name = ""
    client_address = ""

    # date = order_obj.pagos.fecha
    # _format_time = datetime.now().strftime("%H:%M %p")
    # _format_date = date.strftime("%d/%m/%Y")

    I = Image(LOGO)
    I.drawHeight = inch * 0.9
    I.drawWidth = inch * 0.9

    style_table_1 = [
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('SPAN', (0, 0), (0, -1)),
        ('FONTSIZE', (0, 0), (0, 0), 12),
        ('ALIGNMENT', (0, 0), (0, 0), 'LEFT'),  # second column
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # all columns

    ]

    colwiths_table_1 = [_wt * 0.60 * 20 / 100, _wt * 0.60 * 80 / 100]
    rowwiths_table_1 = [inch * 0.6, inch * 0.2, inch * 0.2, inch * 0.2]

    p1_0 = Paragraph(f'COLEGIO MÉDICO VETERINARIO DEPARTAMENTAL AREQUIPA', styles["Center-titulo"])
    p1_1 = Paragraph(f'RPC. 974542692 - RPM. #966239489', styles["Center"])
    p1_2 = Paragraph(f'E-mail: cmveterinarioaqp@gmail.com', styles["Center"])
    p1_3 = Paragraph(f'Facebook: Cmvd arequipa', styles["Center"])
    ana_c1 = Table(
        [(I, p1_0)] +
        [('', p1_1)] +
        [('', p1_2)] +
        [('', p1_3)],
        colWidths=colwiths_table_1, rowHeights=rowwiths_table_1)
    ana_c1.setStyle(TableStyle(style_table_1))

    style_table_2 = [
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('SPAN', (0, 0), (1, 0)),
        ('TOPPADDING', (0, 0), (0, 0), 0),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('RIGHPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0),

    ]

    colwiths_table_2 = [_wt * 0.60 * 25 / 100, _wt * 0.60 * 75 / 100]
    rowwiths_table_2 = [inch * 1.2, inch * 0.2, inch * 0.2]
    p2_0 = Paragraph(f'Señor(es):', styles["Left-name"])
    p2_1 = Paragraph(f'Dirección:', styles["Left-name"])
    p2_2 = Paragraph(f'Dr. {DOCTOR.get_full_name()}', styles["Left-datos"])
    p2_3 = Paragraph(f'Av. {DOCTOR.get_full_name()}', styles["Left-datos"])
    ana_c2 = Table(
        [(ana_c1, '')] +
        [(p2_0, p2_2)] +
        [(p2_1, p2_3)],
        colWidths=colwiths_table_2, rowHeights=rowwiths_table_2)
    ana_c2.setStyle(TableStyle(style_table_2))

    """
    style_table_3 = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightskyblue),
        ('TOPPADDING', (0, 0), (0, 0), 0)

    ]

    colwiths_table_3 = [_wt*0.40 * 100 / 100]
    p3_0 = Paragraph(f'RECIBO', styles["Center"])
    p3_1 = Paragraph(f'N° 000174', styles["Center"])
    ana_c3 = Table(
        [(p3_0,)] +
        [(p3_1,)],
        colWidths=colwiths_table_3)
    ana_c3.setStyle(TableStyle(style_table_3))
    """

    style_table_4 = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.steelblue),
        ('BACKGROUND', (1, 2), (-1, 2), colors.lightskyblue),
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (0, 1), (-1, 1)),
        ('SPAN', (0, 2), (0, -2)),
        ('SPAN', (1, -1), (-1, -1)),
    ]

    colwiths_table_4 = [_wt * 0.40 * 34 / 100, _wt * 0.40 * 22 / 100, _wt * 0.40 * 22 / 100, _wt * 0.40 * 22 / 100]
    rowwiths_table_4 = [inch * 0.3, inch * 0.7, inch * 0.2, inch * 0.2, inch * 0.2]
    p3_0 = Paragraph(f'RECIBO', styles["Center-recibo"])
    p3_1 = Paragraph(f'N° {str(PAGO.id).zfill(6)}', styles["Center-id"])
    p4_0 = Paragraph(f'AREQUIPA', styles["Center-arequipa"])
    p4_1 = Paragraph(f'DIA', styles["Center-ng"])
    p4_2 = Paragraph(f'MES', styles["Center-ng"])
    p4_3 = Paragraph(f'AÑO', styles["Center-ng"])
    p4_4 = Paragraph(f'{PAGO.fecha.day}', styles["Center-datos"])
    p4_5 = Paragraph(f'{PAGO.fecha.month}', styles["Center-datos"])
    p4_6 = Paragraph(f'{PAGO.fecha.year}', styles["Center-datos"])
    p4_7 = Paragraph(f'N° C.M.V.P', styles["Center"])
    p4_8 = Paragraph(f'{DOCTOR.num_CMVP}', styles["Center-datos"])
    ana_c4 = Table(
        [(p3_0, '', '', '')] +
        [(p3_1, '', '', '')] +
        [(p4_0, p4_1, p4_2, p4_3)] +
        [('', p4_4, p4_5, p4_6)] +
        [(p4_7, p4_8, p4_8, p4_8)],
        colWidths=colwiths_table_4, rowHeights=rowwiths_table_4)
    ana_c4.setStyle(TableStyle(style_table_4))

    style_table_5 = [
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.green),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]

    colwiths_table_5 = [_wt * 60 / 100, _wt * 40 / 100]
    ana_c5 = Table(
        [(ana_c2, ana_c4)],
        colWidths=colwiths_table_5)
    ana_c5.setStyle(TableStyle(style_table_5))

    style_table_6 = [
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (-2, -2), (-2, -2), colors.lightskyblue),
        ('BACKGROUND', (0, 0), (3, 0), colors.lightskyblue),
        ('SPAN', (2, -1), (-1, -1)),
        ('SPAN', (0, -2), (1, -1)),
    ]
    TOTAL = 0

    fecha_anterior = f'{DOCTOR.fecha_pagado}'
    if num_cuotas:
        f1 = date.fromisoformat(fecha_anterior) - relativedelta(months=PAGO.num_cuotas - 1)
        mes = f'{MONTH[f1.month - 1]}/{f1.year} - {MONTH[DOCTOR.fecha_pagado.month - 1]}/{DOCTOR.fecha_pagado.year}'

        TOTAL_CUOTAS = PAGO.monto * PAGO.num_cuotas
        TOTAL += TOTAL_CUOTAS

        P_U = Paragraph(f'{PAGO.monto:.2f}', styles["Center-datos"])
        P_T = Paragraph(f'{TOTAL_CUOTAS:.2f}', styles["Center-datos"])
        CANT = Paragraph(f'{PAGO.num_cuotas}', styles["Center-datos"])
    else:
        mes = ''
        P_U = ''
        P_T = ''
        CANT = ''

    cant_vacum = ''
    cant_salud = ''
    cant_quir = ''
    cant_habil = ''

    pu_vacum = ''
    pu_salud = ''
    pu_quir = ''
    pu_habil = ''

    st_vacum = ''
    st_salud = ''
    st_quir = ''
    st_habil = ''

    lote_vacum = ''
    lote_salud = ''
    lote_quir = ''
    lote_habil = ''

    if sales:
        for i in sales:
            if i.certificate.id == 1:
                cant_vacum = Paragraph(f'{i.quantity}', styles["Center-datos"])
                pu_vacum = Paragraph(f'{i.price_unit}', styles["Center-datos"])
                st_vacum = Paragraph(f'{i.price_unit * i.quantity}', styles["Center-datos"])
                TOTAL += (i.price_unit * i.quantity)
                for j in i.list_lots.all():
                    lote_vacum += f'[{j.start}-{j.end}] '
            if i.certificate.id == 2:
                cant_salud = Paragraph(f'{i.quantity}', styles["Center-datos"])
                pu_salud = Paragraph(f'{i.price_unit}', styles["Center-datos"])
                st_salud = Paragraph(f'{i.price_unit * i.quantity}', styles["Center-datos"])
                TOTAL += (i.price_unit * i.quantity)
                for j in i.list_lots.all():
                    lote_salud += f'[{j.start}-{j.end}] '
            if i.certificate.id == 3:
                cant_quir = Paragraph(f'{i.quantity}', styles["Center-datos"])
                pu_quir = Paragraph(f'{i.price_unit}', styles["Center-datos"])
                st_quir = Paragraph(f'{i.price_unit * i.quantity}', styles["Center-datos"])
                TOTAL += (i.price_unit * i.quantity)
                for j in i.list_lots.all():
                    lote_quir += f'[{j.start}-{j.end}] '
            if i.certificate.id == 4:
                cant_habil = Paragraph(f'{i.quantity}', styles["Center-datos"])
                pu_habil = Paragraph(f'{i.price_unit}', styles["Center-datos"])
                st_habil = Paragraph(f'{i.price_unit * i.quantity}', styles["Center-datos"])
                TOTAL += (i.price_unit * i.quantity)
                for j in i.list_lots.all():
                    lote_habil += f'[{j.start}-{j.end}] '

    TOTAL = Paragraph(f'{TOTAL:.2f}', styles["Center-datos"])

    colwiths_table_6 = [_wt * 15 / 100, _wt * 55 / 100, _wt * 15 / 100, _wt * 15 / 100]
    p6_0 = Paragraph(f'CANT.', styles["Center-ng"])
    p6_1 = Paragraph(f'DESCRIPCIÓN', styles["Center-ng"])
    p6_2 = Paragraph(f'P. UNIT.', styles["Center-ng"])
    p6_3 = Paragraph(f'IMPORTE', styles["Center-ng"])
    p6_4 = Paragraph(f'Inscripción Colegiatura', styles["Left"])
    p6_5 = Paragraph(f'Cuota Ordinaria: {mes}', styles["Left"])
    p6_6 = Paragraph(f'Cert. Vacum. : {lote_vacum}', styles["Left"])
    p6_7 = Paragraph(f'Cert. Salud : {lote_salud}', styles["Left"])
    p6_8 = Paragraph(f'Cert. Int. Quir. : {lote_quir}', styles["Left"])
    p6_9 = Paragraph(f'FAF', styles["Left"])
    p6_10 = Paragraph(f'Certificado de Habilidad: {lote_habil}', styles["Left"])
    p6_11 = Paragraph(f'Otros', styles["Left"])
    p6_12 = Paragraph(f'CANCELADO<br/><br/>{PAGO.get_fecha()}', styles["Center-fecha"])
    p6_13 = Paragraph(f'TOTAL S/', styles["Center-ng"])

    ana_c6 = Table(
        [(p6_0, p6_1, p6_2, p6_3)] +
        [('', p6_4, '', '')] +
        [(CANT, p6_5, P_U, P_T)] +
        [(cant_vacum, p6_6, pu_vacum, st_vacum)] +
        [(cant_salud, p6_7, pu_salud, st_salud)] +
        [(cant_quir, p6_8, pu_quir, st_quir)] +
        [('', p6_9, '', '')] +
        [(cant_habil, p6_10, pu_habil, st_habil)] +
        [('', p6_11, '', '')] +
        [(p6_12, '', p6_13, TOTAL)] +
        [('', '', '', '')],
        colWidths=colwiths_table_6)
    ana_c6.setStyle(TableStyle(style_table_6))

    """
    colwiths_table = [_wt * 80 / 100, _wt * 20 / 100]
    p0 = Paragraph(f'{PAGO.id}', styles["Left"])
    p01 = Paragraph(f'974542692', styles["Left"])
    p02 = Paragraph(f'#966239489', styles["Left"])
    p03 = Paragraph(f'cmveterinarioaqp@gmail.com', styles["Left"])
    p04 = Paragraph(f'Cmvd arequipa', styles["Left"])
    ana_c1 = Table(
        [('N° de RECIBO: ', p0)],
        colWidths=colwiths_table)

    ana_c1.setStyle(TableStyle(style_table))
    """

    _dictionary = []
    # _dictionary.append(I)
    _dictionary.append(Spacer(1, 5))
    _dictionary.append(Spacer(-2, -2))
    _dictionary.append(ana_c5)
    _dictionary.append(Spacer(8, 8))
    _dictionary.append(ana_c6)
    _dictionary.append(Spacer(-4, -4))
    _dictionary.append(Spacer(-2, -2))
    buff = io.BytesIO()

    pz_matricial = (2.57 * inch, 11.6 * inch)
    # pz_termical = (3.14961 * inch, 11.6 * inch)
    pz_termical = (BASE * inch, ALTURA * inch)

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
        DOCTOR.nombres + '-' + str(PAGO.id))

    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie('bp', value=pk, expires=expires)

    response.write(buff.getvalue())

    buff.close()
    return response
