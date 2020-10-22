# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductUomCode(models.Model):
	_name = 'product.uom.code'

	name = fields.Char(string='Name')
	code = fields.Char(string='Code')
