# -*- coding: utf-8 -*-
# Copyright 2018 Dominic Krimmer
# Copyright 2019 Joan Marín <Github@JoanMarin>
# Copyright 2019 Diego Carvajal <Github@diegoivanc>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrSequenceDateRange(models.Model):
    _inherit = 'ir.sequence.date_range'

    dian_type = fields.Selection(
        string='DIAN Type',
        related='sequence_id.dian_type',
        store=False)
    # technical_key = fields.Char(string="Technical Key")
    puntoDeVentaId = fields.Char(string='Punto de Venta', help='Identificador en COMFIAR del punto de venta/serie/prefijo asociado al comprobante a procesar; tipo de dato numérico. Nota: consultar identificador al implementador.')
