# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@Diegoivanc>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial_name = fields.Char(string='Commercial Name')

    def name_get(self):
        rec = super(ResPartner, self).name_get()
        res = []

        for partner in rec:
            partner_id = self.env['res.partner'].browse(partner[0])
            name = partner[1]

            if partner_id.commercial_name:
                name = '[%s] %s' % (partner_id.commercial_name, name)
            
            res.append((partner_id.id, name))

        return res

    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name', 'commercial_name')
    def _compute_display_name(self):
        return super(ResPartner, self)._compute_display_name()
