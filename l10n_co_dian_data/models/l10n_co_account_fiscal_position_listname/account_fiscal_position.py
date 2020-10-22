# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountFiscalPosition(models.Model):
	_inherit = 'account.fiscal.position'

	listname = fields.Selection(
        [('48', 'Impuesto sobre las ventas – IVA'), ('49', 'No responsable de IVA')],
        string='Fiscal Regime',
        default=False)
