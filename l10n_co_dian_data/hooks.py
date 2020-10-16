
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, _):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        env["res.partner"]._install_partner_firstname()
