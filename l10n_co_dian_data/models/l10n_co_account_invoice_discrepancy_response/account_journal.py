# -*- coding: utf-8 -*-
# Copyright 2017 Marlon Falcón Hernandez
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    debit_note_sequence = fields.Boolean(
        string="Dedicated Debit Note Sequence",
        help="Check this box if you don't want to share the same sequence for invoices and debit "
             "notes made from this journal",
        default=False)
    debit_note_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Debit Note Entry Sequence",
        help="This field contains the information related to the numbering of the debit note "
             "entries of this journal.",
        copy=False)

    def write(self, vals):
        if vals.get('refund_sequence'):
            for journal in self.filtered(
                    lambda j: j.type in ('sale', 'purchase')
                              and not j.refund_sequence_id):
                journal_vals = {
                    'name': _('Credit Note Sequence - ') + journal.name,
                    'company_id': journal.company_id.id,
                    'code': journal.code}
                journal.refund_sequence_id = self.sudo()._create_sequence(
                    journal_vals,
                    refund=True).id

        if vals.get('debit_note_sequence'):
            for journal in self.filtered(
                    lambda j: j.type in ('sale', 'purchase')
                              and not j.debit_note_sequence_id):
                journal_vals = {
                    'name': _('Debit Note Sequence - ') + journal.name,
                    'company_id': journal.company_id.id,
                    'code': journal.code}
                journal.debit_note_sequence_id = self.sudo()._create_sequence(
                    journal_vals,
                    refund=True).id

        return super(AccountJournal, self).write(vals)