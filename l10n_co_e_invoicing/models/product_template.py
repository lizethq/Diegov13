# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _default_product_scheme(self):
        return self.env['product.scheme'].search([('code', '=', '999' )]).id

    margin_percentage = fields.Float(
        string='Margin Percentage',
        help='The cost price + this percentage will be the reference price',
        digits=dp.get_precision('Discount'),
        default=10)
    reference_price = fields.Float(
        string='Reference Price',
        help='use this field if the reference price does not depend on the cost price',
        digits=dp.get_precision('Product Price'))
    product_scheme_id = fields.Many2one(
        comodel_name='product.scheme',
        string='Product Scheme',
        default=_default_product_scheme)