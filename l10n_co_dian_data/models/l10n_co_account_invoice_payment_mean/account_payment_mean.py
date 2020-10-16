# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _

class AccountPaymentMean(models.Model):
	_name = 'account.payment.mean'
	_description = 'Ways to pay'

	name = fields.Char(string='Name', required=True, translate=True)
	code = fields.Char(string='Code', required=True)

	_sql_constraints = [
		('name_unique', 'unique(name)', _("The name must be unique")),
		('code_unique', 'unique(code)', _("The code must be unique"))]
