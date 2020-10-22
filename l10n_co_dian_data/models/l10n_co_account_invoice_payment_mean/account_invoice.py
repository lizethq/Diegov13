# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
	_inherit = "account.move"

	payment_mean_id = fields.Many2one(
		comodel_name='account.payment.mean',
		string='Payment Method',
		copy=False,
		default=False)

	payment_mean_code_id = fields.Many2one('account.payment.mean.code',
		string='Mean of Payment',
		copy=False,
		default=False)


	def write(self, vals):
		res = super(AccountInvoice, self).write(vals)

		if vals.get('invoice_date'):
			for invoice in self:
				invoice._onchange_invoice_dates()
		
		return res

	@api.onchange('invoice_date', 'date_due', 'invoice_payment_term_id')
	def _onchange_invoice_dates(self):
		payment_mean_obj = self.env['ir.model.data']
		time = 0
		if self.invoice_payment_term_id:
			time = sum([x.days for x in self.invoice_payment_term_id.line_ids])
		
		if not self.invoice_date:
			payment_mean_id = False
		elif (self.invoice_date == self.invoice_date_due and not self.invoice_payment_term_id) \
			or (self.invoice_payment_term_id and time == 0):
			id_payment_mean = payment_mean_obj.get_object_reference(
				'l10n_co_dian_data',
				'account_payment_mean_1')[1]
			payment_mean_id = self.env['account.payment.mean'].browse(id_payment_mean)
		else:
			id_payment_mean = payment_mean_obj.get_object_reference(
				'l10n_co_dian_data',
				'account_payment_mean_2')[1]
			payment_mean_id = self.env['account.payment.mean'].browse(id_payment_mean)

		self.payment_mean_id = payment_mean_id
	
	@api.onchange('partner_id')
	def _onchange_partner_id(self):
		res = super(AccountInvoice, self)._onchange_partner_id()
		self._onchange_invoice_dates()
		return res
