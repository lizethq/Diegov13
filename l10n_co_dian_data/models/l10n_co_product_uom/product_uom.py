# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductUom(models.Model):
	_inherit = 'uom.uom'
	_description = 'measurement units'

	product_uom_code_id = fields.Many2one(
		comodel_name='product.uom.code',
		string='Unit of Measure Code')
