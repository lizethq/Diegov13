# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# Copyright 2019 Diego Carvajal <Github@diegoivanc>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountTaxGroup(models.Model):
	_inherit = "account.tax.group"

	is_einvoicing = fields.Boolean(
		string="Does it Apply for E-Invoicing?",
		default=True)
