# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_einvoicing = fields.Boolean(string='electronic invoicing?')
    resolution_text = fields.Text(string='Resolución')
    
