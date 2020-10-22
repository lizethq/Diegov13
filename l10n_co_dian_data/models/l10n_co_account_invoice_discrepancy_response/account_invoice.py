# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoice(models.Model):
	_inherit = "account.move"

	discrepancy_response_code_id   = fields.Many2one(
		comodel_name='account.invoice.discrepancy.response.code',
		string='Correction concept for Refund Invoice',)

	refund_type = fields.Selection(
		[('debit', 'Debit Note'),
		 ('credit', 'Credit Note')],
		index=True,
		string='Refund Type',
		track_visibility='always')
	
	def _get_sequence(self):
		''' Return the sequence to be used during the post of the current move.
		:return: An ir.sequence record or False.
		'''
		
		res = super(AccountInvoice, self)._get_sequence()
		journal = self.journal_id
		if self.type == 'out_refund' and self.refund_type == 'debit' and journal.debit_note_sequence_id:
			return journal.debit_note_sequence_id
		return res



