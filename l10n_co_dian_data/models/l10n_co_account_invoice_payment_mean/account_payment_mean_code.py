# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _

class AccountPaymentMeanCode(models.Model):
	_name = 'account.payment.mean.code'
	_description = 'Payment methods'

	name = fields.Char(string='Name', required=True, translate=True)
	code = fields.Char(string='Code', required=True)

	_sql_constraints = [(
		'code_and_name_unique',
		'unique(code, name)',
		_("The combination of code and name must be unique"))]
