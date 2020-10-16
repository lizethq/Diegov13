# -*- coding: utf-8 -*-
import pyotp
import logging

import odoo
from odoo import http, _
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.http import request
from passlib.context import CryptContext

default_crypt_context = CryptContext(
    ['pbkdf2_sha512', 'md5_crypt'],
    deprecated=['md5_crypt'],
)

_logger = logging.getLogger(__name__)


class WebHome(Home):
    # Override
    @http.route('/web/login', type='http', auth="none", sitemap=False)
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            if values.get('send_mail') and values.get('send_mail') == "send":
                user = request.env['res.users'].sudo().search([('login','ilike',values['login'])])[0]
                user.twoFA_code = pyotp.random_base32()
                template_id = request.env.ref('auth_2FA.user_auth_2fa_email').id
                request.env['mail.template'].sudo().browse(template_id).send_mail(user.id, force_send=True)
            old_uid = request.uid
            try:
                request.env.cr.execute(
                    '''
                        SELECT id,
                               COALESCE(company_id, NULL), 
                               COALESCE(password, ''), 
                               COALESCE(otp_first_use, TRUE) 
                        FROM res_users 
                        WHERE login=%s
                    ''',
                    [request.params['login']]
                )
                res = request.env.cr.fetchone()
                if not res:
                    raise odoo.exceptions.AccessDenied(_('Wrong login account'))
                [user_id, company_id, hashed, otp_first_use] = res
                if company_id and request.env['res.company'].sudo().browse(company_id).is_open_2fa:
                    # Verify password correctness
                    valid, replacement = default_crypt_context.verify_and_update(request.params['password'], hashed)
                    if replacement is not None:
                        self._set_encrypted_password(self.env.user.id, replacement)
                    if valid:
                        if otp_first_use:
                            values['QRCode'] = 'data:image/png;base64,' + request.env['res.users'].sudo().browse(
                                user_id).otp_qrcode.decode('ascii')
                            values['text'] = _('You are the first time to use OTP,' 
                                               'please scan the QRCode to get validation code.'
                                               'you should store this QRCode image and take good care of it! ')
                        response = request.render('auth_2FA.2fa_auth', values)
                        response.headers['X-Frame-Options'] = 'DENY'
                        return response
                    else:
                        raise odoo.exceptions.AccessDenied()
                # Two-factor authentication is not turned on
                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                   request.params['password'])
                request.params['login_success'] = True
                return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        # otherwise no real way to test debug mode in template as ?debug =>
        # values['debug'] = '' but that's also the fallback value when
        # missing variables in qweb

        if 'debug' in values:
            values['debug'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route('/web/login/2fa_auth', type='http', auth="none")
    def web_login_2fa_auth(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        old_uid = request.uid
        try:
            uid = request.session.authenticate(request.session.db, request.params['login'],
                                               request.params['password'])
            request.params['login_success'] = True
            if values['tfa_code'] and len(values['tfa_code']) == 16:
                request.env['res.users'].sudo().browse(uid).otp_first_use = False if \
                    not request.env['res.users'].sudo().browse(uid).otp_first_use else \
                        request.env['res.users'].sudo().browse(uid).otp_first_use
            else:
                request.env['res.users'].sudo().browse(uid).otp_first_use = False
            return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
        except odoo.exceptions.AccessDenied as e:
            request.uid = old_uid
            if e.args == odoo.exceptions.AccessDenied().args:
                values['error'] = _("Wrong login/password")
            else:
                values['error'] = e.args[0]
        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if 'debug' in values:
            values['debug'] = True

        response = request.render('auth_2FA.2fa_auth', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class AuthSignupHome2FA(AuthSignupHome):

    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
        user = request.env['res.users'].sudo().search([('login', 'ilike', login)])[0]
        if user.company_id and user.company_id.is_open_2fa:
            user.twoFA_code = pyotp.random_base32()
            template_id = request.env.ref('auth_2FA.user_auth_2fa_email').id
            request.env['mail.template'].sudo().browse(template_id).send_mail(user.id, force_send=True)
            res = request.render('auth_2FA.2fa_auth', values)
            return res
        else:
            uid = request.session.authenticate(db, login, password)
            if not uid:
                raise SignupError(_('Authentication Failed.'))
