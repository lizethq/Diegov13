# -*- coding: utf-8 -*-
# The MIT License
# copyright@misterling(26476395@qq.com)
import base64
import datetime
import pyotp
import pyqrcode
import io

from odoo import models, fields, api, _, tools
from odoo.http import request
from odoo.exceptions import AccessDenied

import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    otp_first_use = fields.Boolean(string="First Use OTP", default=True)
    otp_type = fields.Selection(selection=[('time', _('Time based')), ('count', _('Counter based'))], default='time',
                                string="Type",
                                help="Type of 2FA, time = new code for each period, counter = new code for each login")
    otp_secret = fields.Char(string="Secret", size=16, help='16 character base32 secret',
                             default=lambda self: pyotp.random_base32())
    otp_counter = fields.Integer(string="Counter", default=0)
    otp_digits = fields.Integer(string="Digits", default=6, help="Length of the code")
    otp_period = fields.Integer(string="Period", default=30, help="Seconds to update code")
    otp_qrcode = fields.Binary(compute="_compute_otp_qrcode")

    otp_uri = fields.Char(compute='_compute_otp_uri', string="URI")

    twoFA_code = fields.Char(string="Secret CODE", size=16, help='16 character base32 secret temporal code',
                             default=lambda self: pyotp.random_base32())
    twoFA_date = fields.Datetime('Datetime code', compute='_compute_twoFA_date')

    @api.depends('twoFA_code')
    def _compute_twoFA_date(self):
        for record in self:
            tz_offset = self.env.user.tz_offset if self.env.user.tz_offset else False
            tz = int(tz_offset)/100 if tz_offset else 0
            record.twoFA_date = fields.Datetime.now() + datetime.timedelta(hours=tz,minutes=10)

    def toggle_otp_first_use(self):
        for record in self:
            record.otp_first_use = not record.otp_first_use

    # Generate QR code
    @api.model
    def create_qr_code(self, uri):
        buffer = io.BytesIO()
        qr = pyqrcode.create(uri)
        qr.png(buffer, scale=3)
        return base64.b64encode(buffer.getvalue()).decode()

    # Assign the value of QR code to the otp_qrcode variable
    @api.depends('otp_uri')
    def _compute_otp_qrcode(self):
        for record in self:
            record.otp_qrcode = record.create_qr_code(record.otp_uri)

    # Calculating otp_uri
    @api.depends('otp_type', 'otp_period', 'otp_digits', 'otp_secret', 'company_id', 'otp_counter')
    def _compute_otp_uri(self):
        for record in self:
            if record.otp_type == 'time':
                record.otp_uri = pyotp.utils.build_uri(secret=record.otp_secret, name=record.login,
                                                     issuer_name=record.company_id.name, period=record.otp_period)
            else:
                record.otp_uri = pyotp.utils.build_uri(secret=record.otp_secret, name=record.login,
                                                     initial_count=record.otp_counter, issuer_name=record.company_id.name,
                                                     digits=record.otp_digits)

    # Verify otp verification code is correct
    @api.model
    def check_otp(self, otp_code):
        res_user = self.env['res.users'].browse(self.env.uid)
        if type(otp_code) is str and len(otp_code) == 16:
            tz_offset = self.env.user.tz_offset if self.env.user.tz_offset else False
            tz = int(tz_offset)/100 if tz_offset else 0
            now = fields.Datetime.now() + datetime.timedelta(hours=tz)
            return res_user.twoFA_code == otp_code and now < res_user.twoFA_date
        elif type(otp_code) is str and len(otp_code) != 6:
            return False
        if res_user.otp_type == 'time':
            totp = pyotp.TOTP(res_user.otp_secret)
            return totp.verify(otp_code)
        elif res_user.otp_type == 'count':
            hotp = pyotp.HOTP(res_user.otp_secret)
            # Allow users to accidentally click 20 times more, but the code that has been used cannot be used again
            for count in range(res_user.otp_counter, res_user.otp_counter + 20):
                if count > 0 and hotp.verify(otp_code, count):
                    res_user.otp_counter = count + 1
                    return True
        return False

    # Override native _check_credentials, increase two-factor authentication
    def _check_credentials(self, password):
        super(ResUsers, self)._check_credentials(password)
        # Determine whether to turn on two-factor authentication and verify the verification code
        if self.sudo().company_id.is_open_2fa and not self.sudo().check_otp(request.params.get('tfa_code')):
            # pass
            raise AccessDenied(_('Validation Code Error!'))
