# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@joanmarin>
# Copyright 2019 Diego Carvajal <Github@diegoivanc>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from validators import url
from . global_functions import get_pkcs12
from . import global_functions
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from requests import post, exceptions
from lxml import etree

COMFIAR = {
    'prod': 'https://app.comfiar.co/ws/WSComfiar.asmx?wsdl',
    'test': 'http://test.comfiar.co/ws/WSComfiar.asmx?wsdl',
}
xmlns = {
    's': '{http://www.w3.org/2003/05/soap-envelope}',
    'x': '{http://comfiar.com.ar/webservice/}',
}


class ResCompany(models.Model):
    _inherit = "res.company"

    user_comfiar = fields.Char(string='User')
    pwd_comfiar = fields.Char(string='Password')
    sesion_id = fields.Char(string='Id Session')
    date_due_sesion = fields.Char(string='Expiration')
    formatoId = fields.Char(string='Formato Id', help='Identificador en COMFIAR del formato mediante el cual se procesará el comprobante. Nota: consultar identificador al implementador.')
    comfiar_send_mail = fields.Boolean(string='Comfiar sends the email?', default=True, help='By checking this box, the customer information is sent when the invoice is published so that COMFIAR can send it by email.')
    odoo_send_mail_einv = fields.Boolean(string='Odoo sends the email?', default=False, help='Checking this box will send the e-invoicing email from Odoo automatically when validating the status of the DIAN document')
    # pdvid_inv = fields.Char(string='Punto de Venta Inv')
    # pdvid_nc = fields.Char(string='Punto de Venta NC')
    # pdvid_nd = fields.Char(string='Punto de Venta ND')

    einvoicing_enabled = fields.Boolean(string='E-Invoicing Enabled')
    out_invoice_sent = fields.Integer(string='out_invoice Sent')
    out_refund_sent = fields.Integer(string='out_refund Sent')
    in_refund_sent = fields.Integer(string='in_refund Sent')
    profile_execution_id = fields.Selection(
        [('1', 'Production'), ('2', 'Test')],
        'Destination Environment of Document',
        default='2',
        required=True)
    test_set_id = fields.Char(string='Test Set Id')
    software_id = fields.Char(string='Software Id')
    software_pin = fields.Char(string='Software PIN')
    certificate_filename = fields.Char(string='Certificate Filename')
    certificate_file = fields.Binary(string='Certificate File')
    certificate_password = fields.Char(string='Certificate Password')
    signature_policy_url = fields.Char(string='Signature Policy Url')
    signature_policy_description = fields.Char(string='Signature Policy Description')
    signature_policy_filename = fields.Char(string='Signature Policy Filename')
    signature_policy_file = fields.Binary(string='Signature Policy File')
    files_path = fields.Char(string='Files Path')
    einvoicing_email = fields.Char(
        string='E-invoice Email From',
        help="Enter the e-invoice sender's email.")
    einvoicing_partner_no_email = fields.Char(
        string='Failed Emails To',
        help='Enter the email where the invoice will be sent when the customer does not have an email.')
    report_template = fields.Many2one(
        string='Report Template',
        comodel_name='ir.actions.report')
    notification_group_ids = fields.One2many(
        comodel_name='einvoice.notification.group',
        inverse_name='company_id',
        string='Notification Group')
    get_numbering_range_response = fields.Text(string='GetNumberingRange Response')
    tributary_information = fields.Text(string='Información Tributaria')
    attach_pdf = fields.Boolean(string="Adjuntar Pdf", default=False, help='habilita la opción de adjuntar el reporte de factura pdf generado desde Odoo en el comprobante publicado en la plataforma de Comfiar')

    @api.onchange('signature_policy_url')
    def onchange_signature_policy_url(self):
        if not url(self.signature_policy_url):
            raise ValidationError(_('Invalid URL.'))

    # def write(self, vals):
    #     rec = super(ResCompany, self).write(vals)
    #     get_pkcs12(self.certificate_file, self.certificate_password)

    #     return rec


    def _get_GetNumberingRange_values(self):
        xml_soap_values = global_functions.get_xml_soap_values(
            self.certificate_file,
            self.certificate_password)

        xml_soap_values['accountCode'] = self.partner_id.identification_document
        xml_soap_values['accountCodeT'] = self.partner_id.identification_document
        xml_soap_values['softwareCode'] = self.software_id

        return xml_soap_values

    def action_GetNumberingRange(self):
        msg1 = _("Unknown Error,\nStatus Code: %s,\nReason: %s.")
        msg2 = _("Unknown Error: %s\n.")
        wsdl = 'https://vpfe.dian.gov.co/WcfDianCustomerServices.svc?wsdl'
        s = "http://www.w3.org/2003/05/soap-envelope"

        GetNumberingRange_values = self._get_GetNumberingRange_values()
        GetNumberingRange_values['To'] = wsdl.replace('?wsdl', '')
        xml_soap_with_signature = global_functions.get_xml_soap_with_signature(
            global_functions.get_template_xml(GetNumberingRange_values, 'GetNumberingRange'),
            GetNumberingRange_values['Id'],
            self.certificate_file,
            self.certificate_password)

        try:
            response = post(
                wsdl,
                headers={'content-type': 'application/soap+xml;charset=utf-8'},
                data=etree.tostring(xml_soap_with_signature))

            if response.status_code == 200:
                root = etree.fromstring(response.text)
                response = ''

                for element in root.iter("{%s}Body" % s):
                    response = etree.tostring(element, pretty_print=True)

                if response == '':
                    response = etree.tostring(root, pretty_print=True)

                self.write({'get_numbering_range_response': response})
            else:
                raise ValidationError(msg1 % (response.status_code, response.reason))

        except exceptions.RequestException as e:
            raise ValidationError(msg2 % (e))

        return True
    
    def get_sesion_comfiar(self):
        msg1 = _("Unknown Error,\nStatus Code: %s,\nReason: %s,\n\nContact with your administrator "
                "or you can choose a journal with a Contingency Checkbook E-Invoicing sequence "
                "and change the Invoice Type to 'Factura por Contingencia Facturador'.")
        msg2 = _("Unknown Error: %s\n\nContact with your administrator "
                "or you can choose a journal with a Contingency Checkbook E-Invoicing sequence "
                "and change the Invoice Type to 'Factura por Contingencia Facturador'.")
        wsdl = ''

        if self.profile_execution_id == '1':
            wsdl = COMFIAR['prod']
        else:
            wsdl = COMFIAR['test']
        values = {
            'UserComfiar': self.user_comfiar, 
            'PwdComfiar': self.pwd_comfiar
            }
        xml = global_functions.get_template_xml(values, '1_InicioSesion')
        parser = etree.XMLParser(remove_blank_text=True,)
        root = etree.fromstring(xml.encode("utf-8"), parser=parser)
        try:
            response = post(
                wsdl,
                headers={'content-type': 'application/soap+xml;charset=utf-8'},
                data=etree.tostring(root, encoding="unicode"))
            if response.status_code == 200:
                root = etree.fromstring(response.text.encode('utf-8'))
                result = root.find('{s}Body/{x}IniciarSesionResponse/{x}IniciarSesionResult'.format(s = xmlns['s'], x = xmlns['x']))
                sesion_id = result.find('%sSesionId' % xmlns['x']).text
                date_due = result.find('%sFechaVencimiento' % xmlns['x']).text
                self.write({'sesion_id': sesion_id, 'date_due_sesion': date_due})
            elif response.status_code in (500, 503, 507):
                root = etree.fromstring(response.text.encode('utf-8'))
                code = root.find('{s}Body/{s}Fault/{s}Code/{s}Value'.format(s = xmlns['s'], x = xmlns['x'])).text
                reason = root.find('{s}Body/{s}Fault/{s}Reason/{s}Text'.format(s = xmlns['s'], x = xmlns['x'])).text
                raise ValidationError('Código Error: %s\n\n Razón: %s' % (code, reason))
            else:
                raise ValidationError(msg1 % (response.status_code, response.reason))
        except exceptions.RequestException as e:
            raise ValidationError(msg2 % (e))
