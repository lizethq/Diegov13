# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    @api.depends(
        'price_unit',
        'discount',
        'invoice_line_tax_ids',
        'quantity',
        'product_id',
        'invoice_id.partner_id',
        'invoice_id.currency_id',
        'invoice_id.company_id',
        'invoice_id.date_invoice',
        'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        sign = 1

        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(
                price, currency,
                self.quantity,
                product=self.product_id,
                partner=self.invoice_id.partner_id)

        if taxes:
            self.price_subtotal = price_subtotal_signed = taxes['total_excluded']
        else:
            self.price_subtotal = price_subtotal_signed = self.quantity * price

        if (self.invoice_id.currency_id
                and self.invoice_id.company_id
                and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id):
            price_subtotal_signed = self.invoice_id.currency_id.with_context(
                date=self.invoice_id._get_currency_rate_date()).compute(
                price_subtotal_signed,
                self.invoice_id.company_id.currency_id)

        if (self.invoice_id.type in ['in_refund', 'out_refund']
                and self.invoice_id.refund_type == 'credit'):
            sign = -1

        self.price_subtotal_signed = price_subtotal_signed * sign