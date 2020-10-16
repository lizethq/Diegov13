# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveReversal(models.TransientModel):

    _inherit = "account.move.reversal"

    def _prepare_default_reversal(self, move):
        """ Set the document refund_type as credit note """
        res = super()._prepare_default_reversal(move)
        if move.type and move.type in ('out_invoice','out_refund'):
            res.update({
                'refund_type': 'credit',
                'discrepancy_response_code_id': self.discrepancy_response_code_id.id or False,
                'payment_mean_id': move.payment_mean_id.id or False,
            })
        elif move.type and move.type == 'in_invoice':
            res.update({
                'refund_type': 'debit',
            })
        return res