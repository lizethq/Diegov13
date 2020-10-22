# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    resolution_text = fields.Text(string='Resolución')
    
