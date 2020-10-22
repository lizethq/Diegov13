
from odoo import _, exceptions


class EmptyNamesError(exceptions.ValidationError):
    def __init__(self, record, value=None):
        value = value or _("No name is set.")
        self.record = record
        self._value = value
        self.name = _("Error(s) with partner %d's name.") % record.id
        self.args = (self.name, value)
