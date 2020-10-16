# -*- coding: utf-8 -*-
# Copyright 2018 Dominic Krimmer
# Copyright 2019 Joan Marín <Github@JoanMarin>
# Copyright 2019 Diego Carvajal <Github@diegoivanc>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    dian_type = fields.Selection(
        selection_add=[('e-invoicing', _('E-Invoicing'))])
