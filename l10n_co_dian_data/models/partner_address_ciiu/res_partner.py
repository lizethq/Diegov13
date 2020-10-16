# -*- coding: utf-8 -*-
import re

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

alphabet = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ('L', 'L'),
    ('M', 'M'),
    ('N', 'N'),
    ('Ñ', 'Ñ'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q'),
    ('R', 'R'),
    ('S', 'S'),
    ('T', 'T'),
    ('U', 'U'),
    ('V', 'V'),
    ('W', 'W'),
    ('X', 'X'),
    ('Y', 'Y'),
    ('Z', 'Z')
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    field_1 = fields.Many2one('address.code')
    field_2 = fields.Char()
    field_3 = fields.Selection(alphabet)
    field_4 = fields.Many2one('street.code')
    field_5 = fields.Char()
    field_6 = fields.Selection(alphabet)
    field_7 = fields.Many2one('street.code')
    field_8 = fields.Char()
    field_9 = fields.Many2one('address.code')
    field_10 = fields.Char()
    field_11 = fields.Many2one('address.code')
    field_12 = fields.Char()
    ciiu = fields.Many2many('ciiu.value', 'ciiu_value_res_partner_rel', 'partner_id', 'ciiu_id', string='CIIU')

    @api.onchange('field_1', 'field_2', 'field_3', 'field_4', 'field_5',
                  'field_6', 'field_7', 'field_8', 'field_9', 'field_10',
                  'field_11', 'field_12')
    def _onchange_street(self):
        if self.field_1 or self.field_2 or self.field_3 or self.field_4 or self.field_5 or self.field_6 or \
           self.field_7 or self.field_8 or self.field_9 or self.field_10 or self.field_11 or self.field_12: 
            self.street = "%s %s  %s %s %s %s %s %s %s %s %s %s" % (
                self.field_1.code if self.field_1 else "",
                str(self.field_2 or ''),
                str(self.field_3 if self.field_3 else ""),
                self.field_4.code if self.field_4 else "",
                str(self.field_5 or ''),
                str(self.field_6 if self.field_6 else ""),
                self.field_7.code if self.field_7 else "",
                str(self.field_8 or ''),
                self.field_9.code if self.field_9 else "",
                str(self.field_10 or ''),
                self.field_11.code if self.field_11 else "",
                str(self.field_12  or ''))