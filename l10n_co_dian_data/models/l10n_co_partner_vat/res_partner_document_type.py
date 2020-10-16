# -*- coding: utf-8 -*-
# Copyright 2018 Joan Marín <Github@JoanMarin>
# Copyright 2018 Guillermo Montoya <Github@guillermm>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartnerDocumentType(models.Model):
    _name = 'res.partner.document.type'
    _description = 'Partner Document Type'

    name = fields.Char(
        string='Document Type',
        size=100,
        required=True)
    code = fields.Char(
        string='Code',
        size=2,
        required=True)
    checking_required = fields.Boolean(
        string='VAT Check Required',
        default=False)

    def name_get(self):
        res = []

        for record in self:
            name = u'[%s] %s' % (record.code, record.name)
            res.append((record.id, name))

        return res
