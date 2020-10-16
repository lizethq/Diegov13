# -*- coding: utf-8 -*-
# Copyright 2018 Joan Marín <Github@JoanMarin>
# Copyright 2018 Guillermo Montoya <Github@guillermm>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCountry(models.Model):
    _inherit = 'res.country'

    code_dian = fields.Char('Code DIAN')

    def name_get(self):
        res = []
        for record in self:
            name = u'%s [%s]' % (record.name or '', record.code or '')
            res.append((record.id, name))
    
        return res

    @api.model
    def name_search(self, name, args = None, operator = 'ilike', limit = 100):
        if not args:
            args = []

        if name:
            state = self.search([
                '|',
                '|',
                ('code_dian', operator, name),
                ('name', operator, name),
                ('code', operator, name)] + args, limit = limit)
        else:
            state = self.search([], limit=100)

        return state.name_get()
