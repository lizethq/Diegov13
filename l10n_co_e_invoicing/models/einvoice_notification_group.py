# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class EInvoiceNotificationGroup(models.Model):
	_name = 'einvoice.notification.group'

	name = fields.Char(string='Name')
	email = fields.Char(string='Email')
	company_id = fields.Many2one(comodel_name='res.company', string='Company')

	@api.model
	def create(self, vals):
		rec = super(EInvoiceNotificationGroup, self).create(vals)
		# Check email address is valid or not
		if rec.email:
			if re.match(
					"^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
					rec.email) == None:
				raise ValidationError("Please enter a valid email address")

		return rec

	def write(self, values):
		result = super(EInvoiceNotificationGroup, self).write(values)
		# Check email address is valid or not
		if values.get('email'):
			if re.match(
					"^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
					values.get('email')) == None:
				raise ValidationError("Please enter a valid email address")

		return result
