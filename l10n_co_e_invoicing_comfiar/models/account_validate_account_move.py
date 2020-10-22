from odoo import models, api, _
from odoo.exceptions import UserError


class ValidateAccountMove(models.TransientModel):
    _inherit = "validate.account.move"

    def validate_move(self):
        res = super(ValidateAccountMove, self).validate_move()
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get('active_ids', []))]
        elif self._context.get('active_model') == 'account.journal':
            domain = [('journal_id', '=', self._context.get('active_id'))]
        else:
            raise UserError(_("Missing 'active_model' in context."))

        moves = self.env['account.move'].search(domain).filtered('line_ids')
        move_to_send_to_comfiar = moves.sorted(lambda m: (m.date, m.ref or '', m.id))
        sesion = 1
        for invoice in move_to_send_to_comfiar.filtered(lambda x: x.dian_document_lines.filtered(lambda dian_document: dian_document.state == 'draft')):
            for dian_document in invoice.dian_document_lines.filtered(lambda document: document.state == 'draft'):
                if sesion == 1:
                    dian_document.get_sesion_comfiar()
                    sesion += 1
                try:
                    dian_document.AutorizarComprobanteAsincrono()
                    dian_document.SalidaTransaccion()
                    dian_document.validate_status_document_dian()
                except Exception as e:
                    dian_document.output_comfiar_status_code = 'ERROR'
                    dian_document.output_comfiar_response = 'Ocurrio un error durante la publicación \
                                                            de esta factura. Por favor validar el estado de este \
                                                            documento o reprocesarlo \n\n' + str(e)
        return res