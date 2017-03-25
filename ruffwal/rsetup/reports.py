from geraldo import Report, landscape ,ReportBand, ObjectValue, SystemField,\
        BAND_WIDTH, Label,Line,ReportGroup

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.colors import navy, yellow, red



class Reportchartofacc(Report):
    title = 'Chart Of Account Report \n'
    author = 'Infologic Solutions'

    page_size = A4  #landscape(A4)#
    margin_left = 2*cm
    margin_top = 0.5*cm
    margin_right = 0.5*cm
    margin_bottom = 0.5*cm


    class band_detail(ReportBand):
        height = 0.5*cm
        elements=(
            ObjectValue(attribute_name='accname', left=1.3*cm),
            ObjectValue(attribute_name='acccode', left=14*cm,)
            #ObjectValue(attribute_name='datecreated', left=17*cm,
               # get_value=lambda instance: instance.datecreated.strftime('%d/%m/%Y')),
            )
    class band_page_header(ReportBand):
        height = 2.0*cm
        elements = [
                SystemField(expression='%(report_title)s', top=0.7*cm, left=0, width=BAND_WIDTH,
                    style={'fontName': 'Helvetica-Bold', 'fontSize': 10, 'alignment': TA_CENTER}),
                Label(text="Acc Name", top=1.6*cm, left=1.3*cm),
                Label(text="Acc Code", top=1.6*cm, left=14*cm),
                #Label(text=u"Creation Date", top=1.6*cm, left=17*cm),
                SystemField(expression=u'Page %(page_number)d of %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                SystemField(expression='Ruffwall Company', top=0.1*cm,left=0,
                    width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold','fontSize': 14,'alignment': TA_CENTER}),
                ]
        borders = {'bottom': True}

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='Copyright Ruffwal', top=0.5*cm),
                SystemField(expression=u'Printed in %(now:%Y, %b %d)s at %(now:%H:%M)s', top=0.5*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
                ]
        #borders = {'top': True}

    groups = [
        ReportGroup(attribute_name = 'groupname',
            band_header = ReportBand(
                height = 0.7*cm,
                elements = [
                    ObjectValue(attribute_name='groupname', left=0, top=0.1*cm, width=20*cm,
                        get_value=lambda instance: ' ' + (instance.groupname),
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 12})
                    ],
                borders = {'bottom': True},
                )
            ),
            ReportGroup(attribute_name = 'subgroupname',
            band_header = ReportBand(
                height = 0.7*cm,
                elements = [
                    ObjectValue(attribute_name='subgroupname', left=10, top=0.1*cm, width=20*cm,
                        get_value=lambda instance: ' ' + (instance.subgroupname),
                        style={'fontName': 'Helvetica-Bold', 'fontSize': 10})
                    ],
                borders = {'bottom': True},
                )
            ),
        ]
