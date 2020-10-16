# -*- coding: utf-8 -*-
# Copyright 2018 Joan Marín <Github@JoanMarin>
# Copyright 2018 Guillermo Montoya <Github@guillermm>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError
import re
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    document_type_id = fields.Many2one(
        string = 'Document Type',
        comodel_name = 'res.partner.document.type')
    document_type_code = fields.Char(
            related='document_type_id.code',
            store=False)
    check_digit = fields.Char(string='Verification Digit', size=1)
    identification_document = fields.Char('Identification Document')

    @api.onchange('identification_document')
    def _compute_concat_nit(self):
        """
        Concatenating and formatting the NIT number in order to have it
        consistent everywhere where it is needed
        @return: void
        """
        # Executing only for Document Type 31 (NIT)
        for partner in self:

            _logger.info('document')
            _logger.info(partner.document_type_id.code)
            if partner.document_type_id.code == '31':
                # First check if entered value is valid
                _logger.info('if')
                self._check_ident()
                self._check_ident_num()

                # Instead of showing "False" we put en empty string
                if partner.identification_document == False:
                    partner.identification_document = ''
                else:
                    _logger.info('else')
                    partner.check_digit = ''

                    # Formatting the NIT: xx.xxx.xxx-x
                    s = str(partner.identification_document)[::-1]
                    newnit = '.'.join(s[i:i + 3] for i in range(0, len(s), 3))
                    newnit = newnit[::-1]

                    nitList = [
                        newnit,
                        # Calling the NIT Function
                        # which creates the Verification Code:
                        self._check_dv(str(partner.identification_document))
                    ]

                    formatedNitList = []

                    for item in nitList:
                        if item != '':
                            formatedNitList.append(item)
                            partner.check_digit = '-'.join(formatedNitList)

                    # Saving Verification digit in a proper field
                    for pnitem in self:
                        _logger.info(nitList[1])
                        _logger.info('nitlist')
                        pnitem.check_digit = nitList[1]

    def _check_dv(self, nit):
        """
        Function to calculate the check digit (DV) of the NIT. So there is no
        need to type it manually.
        @param nit: Enter the NIT number without check digit
        @return: String
        """
        for item in self:
            if item.document_type_id.code != '31':
                return str(nit)

            nitString = '0'*(15-len(nit)) + nit
            vl = list(nitString)
            result = (
                int(vl[0])*71 + int(vl[1])*67 + int(vl[2])*59 + int(vl[3])*53 +
                int(vl[4])*47 + int(vl[5])*43 + int(vl[6])*41 + int(vl[7])*37 +
                int(vl[8])*29 + int(vl[9])*23 + int(vl[10])*19 + int(vl[11])*17 +
                int(vl[12])*13 + int(vl[13])*7 + int(vl[14])*3
            ) % 11

            if result in (0, 1):
                return str(result)
            else:
                return str(11-result)


    @api.onchange('identification_document')
    def _check_ident(self):
        """
        This function checks the number length in the Identification field.
        Min 6, Max 12 digits.
        @return: void
        """
        for item in self:
            if item.document_type_id.code != 1:
                msg = _('Error! Number of digits in Identification number must be'
                        'between 2 and 12')
                if len(str(item.identification_document)) < 2:
                    raise exceptions.ValidationError(msg)
                elif len(str(item.identification_document)) > 12:
                    raise exceptions.ValidationError(msg)

    @api.constrains('identification_document')
    def _check_ident_num(self):
        """
        This function checks the content of the identification fields: Type of
        document and number cannot be empty.
        There are two document types that permit letters in the identification
        field: 21 and 41. The rest does not permit any letters
        @return: void
        """
        for item in self:
            if item.document_type_id.code != 1:
                if item.identification_document is not False and \
                                item.document_type_id.code != 21 and \
                                item.document_type_id.code != 41:
                    if re.match("^[0-9]+$", item.identification_document) is None:
                        msg = _('Error! Identification number can only '
                                'have numbers')
                        raise exceptions.ValidationError(msg)



    @api.onchange('country_id', 'identification_document', 'check_digit', 'document_type_id')
    def _onchange_vat(self):
        if self.country_id and self.identification_document:
            if self.country_id.code:
                if self.check_digit and self.document_type_code == '31':
                    self.vat = self.country_id.code + self.identification_document + self.check_digit
                elif self.document_type_code == '43':
                    self.check_digit = False
                    self.vat = 'CO' + self.identification_document
                else:
                    self.check_digit = False
                    self.vat = self.country_id.code + self.identification_document
            else:
                msg = _('The Country has No ISO Code.')
                raise ValidationError(msg)
        elif not self.identification_document and self.vat:
            self.vat = False

    @api.constrains('vat', 'document_type_id', 'country_id')
    def check_vat(self):
        def _checking_required(partner):
            '''
            Este método solo aplica para Colombia y obliga a seleccionar
            un tipo de documento de identidad con el fin de determinar
            si es verificable por el algoritmo VAT. Si no se define,
            de todas formas el VAT se evalua como un NIT.
            '''
            return ((partner.document_type_id and \
                partner.document_type_id.checking_required) or \
                not partner.document_type_id) == True

        msg = _('The Identification Document does not seems to be correct.')

        for partner in self:
            if not partner.vat:
                continue

            vat_country, vat_number = self._split_vat(partner.vat)

            if partner.document_type_code == '43':
                vat_country = 'co'
            elif partner.country_id:
                vat_country = partner.country_id.code.lower()

            if not hasattr(self, 'check_vat_' + vat_country):
                continue

            #check = getattr(self, 'check_vat_' + vat_country)

            if vat_country == 'co':
                if not _checking_required(partner):
                    continue

            #if check and not check(vat_number):
            #   raise ValidationError(msg)

        return True

    def check_vat_co(self, vat):
        '''
        Check VAT Routine for Colombia.
        '''
        if type(vat) == str:
            vat = vat.replace('-', '', 1).replace('.', '', 2)

        if len(str(vat)) < 4:
            return False

        try:
            int(vat)
        except ValueError:
            return False

        # Validación Sin identificación del exterior
        # o para uso definido por la DIAN
        if len(str(vat)) == 9 and str(vat)[0:5] == '44444' \
            and int(str(vat)[5:]) <= 9000 \
            and int(str(vat)[5:]) >= 4001:

            return True

        prime = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
        sum = 0
        vat_len = len(str(vat))

        for i in range(vat_len - 2, -1, -1):
            sum += int(str(vat)[i]) * prime[vat_len - 2 - i]

        if sum % 11 > 1:
            return str(vat)[vat_len - 1] == str(11 - (sum % 11))
        else:
            return str(vat)[vat_len - 1] == str(sum % 11)
