# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CiiuValue(models.Model):
    _name = 'ciiu.value'
    _description = 'CIIU Optional Value'
    _rec_name = "code"

    code = fields.Char(required=True)
    name = fields.Char(string='Description', required=True)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True, default=lambda self: self.env['res.company']._company_default_get('ciiu.value'))
    
    def name_get(self):
        res = []
        for record in self:
            name = u'%s' % record.code
            res.append((record.id, name))
    
        return res

    @api.model
    def name_search(self, name, args = None, operator = 'ilike', limit = 100):
        if not args:
            args = []

        if name:
            isic = self.search([
                '|',
                ('name', operator, name),
                ('code', operator, name)] + args, limit = limit)
        else:
            isic = self.search(args, limit = limit)

        return isic.name_get()