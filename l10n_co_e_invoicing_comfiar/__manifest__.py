# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@joanmarin>
# Copyright 2019 Diego Carvajal <Github@diegoivanc>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Colombian E-Invoicing with COMFIAR",
    "category": "Financial",
    "version": "10.0.1.0.0",
    "author": "Bernardo D. Lara Guevara bl@todoo.co",
    "website": "http://www.exaap.com",
    "license": "AGPL-3",
    "summary": "Colombian E-Invoicing",
    "depends": ["l10n_co_dian_data",],
    'external_dependencies': {
        'python': [
            'validators',
            'OpenSSL',
            'xades',
        ],
    },
    "data": [
        'security/account_invoice_dian_document_security.xml',
        'security/ir.model.access.csv',
        "data/product_scheme_data.xml",
        "views/account_invoice_views.xml",
        "views/account_journal_views.xml",
        "views/account_invoice_dian_document_views.xml",
        "views/ir_sequence_views.xml",
        "views/res_company_views.xml",
        "views/account_tax_group_views.xml",
        "views/product_template_views.xml",
        "views/res_partner_views.xml",
        "report/account_invoice_report_template.xml",
        "report/account_move_reports.xml",
        "report/account_move_templates.xml",
    ],
    "installable": True,
}
