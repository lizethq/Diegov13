# -*- coding: utf-8 -*-
# Copyright 2016 Dominic Krimmer
# Copyright 2016 Luis Alfredo da Silva (luis.adasilvaf@gmail.com)
# Copyright 2019 Joan Marín <Github@JoanMarin>account.invoice.line
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrSequenceDateRange(models.Model):
    _inherit = 'ir.sequence.date_range'

    use_dian_control = fields.Boolean(
        string='Use DIAN Resolutions Control?',
        related='sequence_id.use_dian_control',
        store=False)
    prefix = fields.Char(string='Prefix')
    resolution_number = fields.Char(string='Resolution Number')
    number_from = fields.Integer( string='Initial Number', default=False)
    number_to = fields.Integer(string='Final Number', default=False)
    active_resolution = fields.Boolean(string='Active Resolution?')
