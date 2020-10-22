# -*- coding: utf-8 -*-
# Copyright 2017 Marlon Falcón Hernandez
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class AccountInvoiceRefund(models.TransientModel):
    """Refunds invoice"""
    _inherit = "account.move.reversal"

    discrepancy_response_code_id = fields.Many2one(
        comodel_name='account.invoice.discrepancy.response.code',
        string='Correction concept for Refund Invoice')
    
    @api.onchange('discrepancy_response_code_id')
    def _onchange_discrepancy_response_code_id(self):
        if self.discrepancy_response_code_id:
            self.reason = self.discrepancy_response_code_id.name
    
    # @api.multi
    # def compute_refund(self, mode='refund'):
    #     inv_obj = self.env['account.invoice']
    #     inv_tax_obj = self.env['account.invoice.tax']
    #     inv_line_obj = self.env['account.invoice.line']
    #     context = dict(self._context or {})
    #     xml_id = False
    #
    #     for form in self:
    #         created_inv = []
    #         date = False
    #         description = False
    #         for inv in inv_obj.browse(context.get('active_ids')):
    #             if inv.state in ['draft', 'cancel']:
    #                 raise UserError(_('Cannot create credit note for the draft/cancelled invoice.'))
    #             if inv.reconciled and mode in ('cancel', 'modify'):
    #                 raise UserError(_(
    #                     'Cannot create a credit note for the invoice which is already reconciled, invoice should be unreconciled first, then only you can add credit note for this invoice.'))
    #
    #             date = form.date or False
    #             description = form.description or inv.name
    #             refund = inv.refund(form.date_invoice, date, description, inv.journal_id.id)
    #
    #             created_inv.append(refund.id)
    #             if mode in ('cancel', 'modify'):
    #                 movelines = inv.move_id.line_ids
    #                 to_reconcile_ids = {}
    #                 to_reconcile_lines = self.env['account.move.line']
    #                 for line in movelines:
    #                     if line.account_id.id == inv.account_id.id:
    #                         to_reconcile_lines += line
    #                         to_reconcile_ids.setdefault(line.account_id.id, []).append(line.id)
    #                     if line.reconciled:
    #                         line.remove_move_reconcile()
    #                 refund.action_invoice_open()
    #                 for tmpline in refund.move_id.line_ids:
    #                     if tmpline.account_id.id == inv.account_id.id:
    #                         to_reconcile_lines += tmpline
    #                 to_reconcile_lines.filtered(lambda l: l.reconciled == False).reconcile()
    #                 if mode == 'modify':
    #                     invoice = inv.read(inv_obj._get_refund_modify_read_fields())
    #                     invoice = invoice[0]
    #                     del invoice['id']
    #                     invoice_lines = inv_line_obj.browse(invoice['invoice_line_ids'])
    #                     invoice_lines = inv_obj.with_context(mode='modify')._refund_cleanup_lines(invoice_lines)
    #                     tax_lines = inv_tax_obj.browse(invoice['tax_line_ids'])
    #                     tax_lines = inv_obj._refund_cleanup_lines(tax_lines)
    #                     invoice.update({
    #                         'type': inv.type,
    #                         'date_invoice': form.date_invoice,
    #                         'state': 'draft',
    #                         'number': False,
    #                         'invoice_line_ids': invoice_lines,
    #                         'tax_line_ids': tax_lines,
    #                         'date': date,
    #                         'origin': inv.origin,
    #                         'fiscal_position_id': inv.fiscal_position_id.id,
    #                     })
    #                     for field in inv_obj._get_refund_common_fields():
    #                         if inv_obj._fields[field].type == 'many2one':
    #                             invoice[field] = invoice[field] and invoice[field][0]
    #                         else:
    #                             invoice[field] = invoice[field] or False
    #                     inv_refund = inv_obj.create(invoice)
    #                     if inv_refund.payment_term_id.id:
    #                         inv_refund._onchange_payment_term_date_invoice()
    #                     created_inv.append(inv_refund.id)
    #             xml_id = inv.type == 'out_invoice' and 'action_invoice_out_refund' or \
    #                      inv.type == 'out_refund' and 'action_invoice_tree1' or \
    #                      inv.type == 'in_invoice' and 'action_invoice_in_refund' or \
    #                      inv.type == 'in_refund' and 'action_invoice_tree2'
    #             # Put the reason in the chatter
    #             subject = _("Credit Note")
    #             body = description
    #             refund.message_post(body=body, subject=subject)
    #     if xml_id:
    #         result = self.env.ref('account.%s' % (xml_id)).read()[0]
    #         invoice_domain = safe_eval(result['domain'])
    #         invoice_domain.append(('id', 'in', created_inv))
    #         result['domain'] = invoice_domain
    #         return result
    #     return True

    def compute_refund(self, mode='refund'):
        msg1 = _('Cannot refund draft/proforma/cancelled invoice.')
        msg2 = _('Cannot refund invoice which is already reconciled, invoice should be '
                 'unreconciled first. You can only refund this invoice.')
        inv_obj = self.env['account.invoice']
        inv_tax_obj = self.env['account.invoice.tax']
        inv_line_obj = self.env['account.invoice.line']
        context = dict(self._context or {})
        xml_id = False

        for form in self:
            created_inv = []
            date = False
            description = False

            for inv in inv_obj.browse(context.get('active_ids')):
                if inv.state in ['draft', 'proforma2', 'cancel']:
                    raise UserError(msg1)

                if inv.reconciled and mode in ('cancel', 'modify'):
                    raise UserError(msg2)

                date = form.date or False
                description = form.description or inv.name
                refund = inv.refund(form.date_invoice, date, description, inv.journal_id.id)
                refund.update({
                    'refund_type': 'credit',
                    'discrepancy_response_code_id': form.discrepancy_response_code_id.id,
                    'name': 'credit'})
                created_inv.append(refund.id)

                if mode in ('cancel', 'modify'):
                    movelines = inv.move_id.line_ids
                    to_reconcile_ids = {}
                    to_reconcile_lines = self.env['account.move.line']

                    for line in movelines:
                        if line.account_id.id == inv.account_id.id:
                            to_reconcile_lines += line
                            to_reconcile_ids.setdefault(line.account_id.id, []).append(line.id)
                        if line.reconciled:
                            line.remove_move_reconcile()

                    refund.action_invoice_open()

                    for tmpline in refund.move_id.line_ids:
                        if tmpline.account_id.id == inv.account_id.id:
                            to_reconcile_lines += tmpline

                    to_reconcile_lines.filtered(lambda l: l.reconciled == False).reconcile()

                    if mode == 'modify':
                        invoice = inv.read(inv_obj._get_refund_modify_read_fields())
                        invoice = invoice[0]
                        del invoice['id']
                        invoice_lines = inv_line_obj.browse(invoice['invoice_line_ids'])
                        invoice_lines = inv_obj.with_context(
                            mode='modify')._refund_cleanup_lines(invoice_lines)
                        tax_lines = inv_tax_obj.browse(invoice['tax_line_ids'])
                        tax_lines = inv_obj._refund_cleanup_lines(tax_lines)
                        invoice.update({
                            'type': inv.type,
                            'date_invoice': form.date_invoice,
                            'state': 'draft',
                            'number': False,
                            'invoice_line_ids': invoice_lines,
                            'tax_line_ids': tax_lines,
                            'date': date,
                            'origin': inv.origin,
                            'fiscal_position_id': inv.fiscal_position_id.id})

                        for field in inv_obj._get_refund_common_fields():
                            if inv_obj._fields[field].type == 'many2one':
                                invoice[field] = invoice[field] and invoice[field][0]
                            else:
                                invoice[field] = invoice[field] or False

                        inv_refund = inv_obj.create(invoice)

                        if inv_refund.payment_term_id.id:
                            inv_refund._onchange_payment_term_date_invoice()

                        created_inv.append(inv_refund.id)

                xml_id = (inv.type in ['out_refund', 'out_invoice']) and 'action_invoice_tree1' or \
                         (inv.type in ['in_refund', 'in_invoice']) and 'action_invoice_tree2'
                # Put the reason in the chatter
                subject = _("Invoice Refund")
                body = description
                refund.message_post(body=body, subject=subject)

        if xml_id:
            result = self.env.ref('account.%s' % (xml_id)).read()[0]
            invoice_domain = safe_eval(result['domain'])
            invoice_domain.append(('id', 'in', created_inv))
            result['domain'] = invoice_domain

            return result

        return True