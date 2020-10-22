# -*- coding: utf-8 -*-
{
    'name': 'Two-factor authentication',
    'version': '1.1',
    'category': 'Tools',
    'description': """Two-factor authentication with google authenticator or email code.""",
    'author': 'misterling',
    'contributors': ['Oscar Bolaños ob@todoo.co'],
    'license': 'LGPL-3',
    'depends': ['auth_signup', 'website'],
    'data': [
        'views/res_users.xml',
        'views/view_2FA_auth.xml',
        'views/res_config_settings_views.xml',
        'data/mail_template.xml',
    ],
    'external_dependencies': {
        'python': ['pyotp','pyqrcode','pypng'],
    },
    'installable': True,
    'auto_install': False,
}
