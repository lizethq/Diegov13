# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCoDianData(http.Controller):
#     @http.route('/l10n_co_dian_data/l10n_co_dian_data/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_co_dian_data/l10n_co_dian_data/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_co_dian_data.listing', {
#             'root': '/l10n_co_dian_data/l10n_co_dian_data',
#             'objects': http.request.env['l10n_co_dian_data.l10n_co_dian_data'].search([]),
#         })

#     @http.route('/l10n_co_dian_data/l10n_co_dian_data/objects/<model("l10n_co_dian_data.l10n_co_dian_data"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_co_dian_data.object', {
#             'object': obj
#         })
