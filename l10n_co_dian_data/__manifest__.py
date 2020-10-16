# -*- coding: utf-8 -*-
{
    'name': "DIAN Data Fields",

    'summary': """
        Este módulo contiene la información identificada por la DIAN para la localización Colombiana""",
    'description': """
        - l10n_co_account_fiscal_position_party_tax_scheme: Responsabilidades Fiscales para la localizacion Colombiana.
        - l10n_co_account_invoice_discrepancy_response: Conceptos de corrección para facturas rectificativas para la localizacion Colombiana.
        - l10n_co_account_invoice_payment_mean: Formas y medios de pago para la localizacion Colombiana.
        - l10n_co_account_tax_group_type: Tipos de grupos tributarios colombianos.
        - l10n_co_base_location: Datos colombianos ZIP / ciudades, estados y países.
        - l10n_co_partner_person_type: Tipos de organización jurídica (Personas) para la localizacion Colombiana y manejo de los nombres y apellidos de los contactos.
        - l10n_co_sequence_resolution: Resolución de la DIAN para la secuencia.

        - partner_commercial_name: Nombre comercial del socio.
        - l10n_co_account_fiscal_position_listname: Regímenes fiscales para la localizacion Colombiana.
        - l10n_co_product_uom: Código de unidades Colombiano.
    """,
    'author': "Todoo SAS, "
              "Bernardo D. Lara Guevara bl@todoo.co",
    'website': "https://www.todoo.co/",
    'category': 'Localization',
    'version': '0.1',
    'depends': ['account', 'base_setup', 'base_vat', 'product', 'base_address_city', 'contacts'],
    "post_init_hook": "post_init_hook",
    'data': [
        "security/l10n_co_account_fiscal_position_party_tax_scheme/ir.model.access.csv",
		"data/l10n_co_account_fiscal_position_party_tax_scheme/account_fiscal_position_tax_level_code_data.xml",
		"data/l10n_co_account_fiscal_position_party_tax_scheme/account_fiscal_position_tax_scheme_data.xml",
		"views/l10n_co_account_fiscal_position_party_tax_scheme/account_fiscal_position_tax_level_code_views.xml",
		"views/l10n_co_account_fiscal_position_party_tax_scheme/account_fiscal_position_tax_scheme_views.xml",
		"views/l10n_co_account_fiscal_position_party_tax_scheme/account_fiscal_position_views.xml",

        "security/l10n_co_account_invoice_discrepancy_response/ir.model.access.csv",
		"data/l10n_co_account_invoice_discrepancy_response/account_invoice_discrepancy_response_code_data.xml",
		"wizards/l10n_co_account_invoice_discrepancy_response/account_invoice_debit_note.xml",
		"wizards/l10n_co_account_invoice_discrepancy_response/account_invoice_refund.xml",
		"views/l10n_co_account_invoice_discrepancy_response/account_invoice_discrepancy_response_code_views.xml",
		"views/l10n_co_account_invoice_discrepancy_response/account_invoice_views.xml",
		"views/l10n_co_account_invoice_discrepancy_response/account_journal_views.xml",

        "security/l10n_co_account_invoice_payment_mean/ir.model.access.csv",
		"data/l10n_co_account_invoice_payment_mean/account_payment_mean_data.xml",
		"data/l10n_co_account_invoice_payment_mean/account_payment_mean_code_data.xml",
		"views/l10n_co_account_invoice_payment_mean/account_payment_mean_views.xml",
		"views/l10n_co_account_invoice_payment_mean/account_payment_mean_code_views.xml",
		"views/l10n_co_account_invoice_payment_mean/account_invoice_views.xml",

        'security/l10n_co_account_tax_group_type/ir.model.access.csv',
        "data/l10n_co_account_tax_group_type/account_tax_group_type_data.xml",
        "views/l10n_co_account_tax_group_type/account_tax_group_views.xml",

        "security/l10n_co_base_location/ir.model.access.csv",
        "data/l10n_co_base_location/res_country_data.xml",
        "data/l10n_co_base_location/res_country_state_data.xml",
        # "data/l10n_co_base_location/res.city.csv",
        "data/l10n_co_base_location/res_city_data.xml",
        "data/l10n_co_base_location/res_city_zip_data.xml",
        # "data/l10n_co_base_location/res.city.zip.csv",
        #"data/l10n_co_base_location/res_better_zip_data.xml",
        "views/l10n_co_base_location/res_city_zip_view.xml",
        "views/l10n_co_base_location/res_city_view.xml",
        "views/l10n_co_base_location/res_country_view.xml",
        #"views/l10n_co_base_location/res_country_state_views.xml",
        "views/l10n_co_base_location/res_company_view.xml",
        "views/l10n_co_base_location/res_partner_view.xml",

        "views/l10n_co_partner_person_type/res_config_settings_views.xml",
        "views/l10n_co_partner_person_type/res_partner_views.xml",
        "views/l10n_co_partner_person_type/res_users_views.xml",

        "security/l10n_co_partner_vat/ir.model.access.csv",
        "data/l10n_co_partner_vat/res_partner_document_type_data.xml", 
        "views/l10n_co_partner_vat/res_partner_views.xml",

        "views/l10n_co_sequence_resolution/ir_sequence_views.xml",
        "views/l10n_co_sequence_resolution/account_invoice_views.xml",

        "views/partner_commercial_name/res_partner_views.xml",

        "views/l10n_co_account_fiscal_position_listname/account_fiscal_position_views.xml",

        #"security/l10n_co_product_uom/ir.model.access.csv",
		"data/l10n_co_product_uom/product.uom.code.csv",
		"views/l10n_co_product_uom/product_uom_views.xml",

        "security/partner_address_ciiu/ir.model.access.csv",
        "data/partner_address_ciiu/address_code_data.xml",
        "views/partner_address_ciiu/address_code_views.xml",
        "views/partner_address_ciiu/ciiu_value_views.xml",
        "views/partner_address_ciiu/street_code_views.xml",
        "views/partner_address_ciiu/res_partner_views.xml",
    ],
}
