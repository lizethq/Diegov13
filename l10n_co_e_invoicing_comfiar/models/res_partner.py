# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@joanmarin>
# Copyright 2019 Diego Carvajal <Github@diegoivanc>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
	_inherit = "res.partner"

	check_mail_einv = fields.Boolean(string='Need attachments in e-invoicing mail', default=False,
		help='This check allows to disable the automatic sending of the electronic invoice email at the moment of validating the status of the DIAN document')	

	def _get_accounting_partner_party_values(self):
		msg1 = _("'%s' does not have a person type established.")
		msg2 = _("'%s' does not have a city established.")
		msg3 = _("'%s' does not have a state established.")
		msg4 = _("'%s' does not have a country established.")
		msg5 = _("'%s' does not have a verification digit established.")
		msg6 = _("'%s' does not have a DIAN document type established.")
		msg7 = _("'%s' does not have a identification document established.")
		msg8 = _("'%s' does not have a fiscal position correctly configured.")
		msg9 = _("'%s' does not have a fiscal position established.")
		msg10 = _("E-Invoicing Agent: '%s' does not have a E-Invoicing Email.")
		msg11 = _("The partner '%s' does not have a Email.")
		name = self.name
		zip_code = False
		identification_document = self.identification_document
		first_name = False
		family_name = False
		middle_name = False
		telephone = False

		if not self.person_type:
			raise UserError(msg1 % self.name)

		if self.country_id:
			if self.country_id.code == 'CO' and not self.zip_id:
				raise UserError(msg2 % self.name)
			elif self.country_id.code == 'CO' and not self.state_id:
				raise UserError(msg3 % self.name)
		else:
			raise UserError(msg4 % self.name)

		if self.document_type_id:
			document_type_code = self.document_type_id.code

			if document_type_code == '31' and not self.check_digit:
				raise UserError(msg5 % self.name)

			#Punto 13.2.1. del anexo técnico version 1.8
			if document_type_code not in ('11', '12', '13', '21', '22', '31', '41', '42', '50', '91'):
				if self.person_type == '1':
					raise UserError(msg6 % self.name)
				else:
					name = 'usuario final'
					document_type_code = '13'
					identification_document = '2222222222'
		else:
			raise UserError(msg6 % self.name)


		if not self.identification_document:
			raise UserError(msg7 % self.name)

		if not self.email:
			raise UserError(msg11 % self.name)

		if self.property_account_position_id:
			if (not self.property_account_position_id.tax_level_code_id
					or not self.property_account_position_id.tax_scheme_id
					or not self.property_account_position_id.listname):
				raise UserError(msg8 % self.name)

			tax_level_codes = ''
			# tax_scheme_code = self.property_account_position_id.tax_scheme_id.code
			# tax_scheme_name = self.property_account_position_id.tax_scheme_id.name
		else:
			raise UserError(msg9 % self.name)


		for tax_level_code_id in self.property_account_position_id.tax_level_code_id:
			if tax_level_codes == '':
				tax_level_codes = tax_level_code_id.code
			else:
				tax_level_codes += ';' + tax_level_code_id.code

		if self.firstname:
			first_name = self.firstname
			middle_name = self.othernames
		else:
			first_name = self.othernames

		if self.lastname and self.lastname2:
			family_name = self.lastname + self.lastname2
		elif self.lastname:
			family_name = self.lastname
		elif self.lastname2:
			family_name = self.lastname2

		if self.phone and self.mobile:
			telephone = self.phone + " / " + self.mobile
		elif self.lastname:
			telephone = self.phone
		elif self.lastname2:
			telephone = self.mobile


		return {
			'AdditionalAccountID': self.person_type,
			'PartyName': self.commercial_name,
			'Name': self.name,
			'AddressID': self.zip_id.dian_code or '',
			'AddressCityName':  self.zip_id.city_id.name or '',
			'AddressPostalZone': self.zip_id.dian_code or '',
			'AddressCountrySubentity': self.state_id.name,
			'AddressCountrySubentityCode': self.state_id.code,
			'AddressLine': self.street or '',
			'CompanyIDschemeID': self.check_digit,
			'CompanyIDschemeName': self.document_type_id.code,
			'CompanyID': self.identification_document,
			'listName': self.property_account_position_id.listname,
			'TaxLevelCode': self.property_account_position_id.tax_level_code_id.code,
			'TaxSchemeID': self.property_account_position_id.tax_scheme_id.code,
			'TaxSchemeName': self.property_account_position_id.tax_scheme_id.name,
			'CorporateRegistrationSchemeName': self.ref,
			'CountryIdentificationCode': self.country_id.code,
			'CountryName': self.country_id.name,
			'FirstName': first_name,
			'FamilyName': family_name,
			'MiddleName': middle_name,
			'Telephone': telephone,
			'Telefax': '',
			'ElectronicMail': self.email
		}


	def _get_tax_representative_party_values(self):
		return {
			'IDschemeID': self.check_digit,
			'IDschemeName': self.document_type_id.code,
			'ID': self.identification_document}

	def _get_delivery_values(self):
		msg1 = _("'%s' does not have a city established.")
		msg2 = _("'%s' does not have a state established.")
		msg3 = _("'%s' does not have a country established.")
		zip_code = False

		if self.country_id:
			if self.country_id.code == 'CO':
				if not self.zip_id:
					raise UserError(msg1 % self.name)
				elif not self.state_id:
					raise UserError(msg2 % self.name)
		else:
			raise UserError(msg3 % self.name)

		return {
			'AddressID': self.zip_id.dian_code or '',
			'AddressCityName': self.zip_id.city_id.name or '',
			'AddressPostalZone': self.zip_id.dian_code or '',
			'AddressCountrySubentity': self.state_id.name or '',
			'AddressCountrySubentityCode': self.state_id.code or '',
			'AddressLine': self.street or '',
			'CountryIdentificationCode': self.country_id.code,
			'CountryName': self.country_id.name}