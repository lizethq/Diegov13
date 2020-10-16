# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductScheme(models.Model):
    _name = 'product.scheme'

    code = fields.Char(string='schemeID')
    name = fields.Char(string='schemeName')
    scheme_agency_id = fields.Char(string='schemeAgencyID')
