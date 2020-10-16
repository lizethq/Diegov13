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



class ResCompany(models.Model):
    _inherit = "res.company"

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
    tributary_information = fields.Text(string='Tributary Information')


    @api.onchange('signature_policy_url')
    def onchange_signature_policy_url(self):
        if not url(self.signature_policy_url):
            raise ValidationError(_('Invalid URL.'))

    def write(self, vals):
        rec = super(ResCompany, self).write(vals)
        get_pkcs12(self.certificate_file, self.certificate_password)

        return rec


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
