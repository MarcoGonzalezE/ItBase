# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ItBaseMensajeWizard(models.TransientModel):
	_name = 'itbase.mensaje.wizard'

	mensaje = fields.Text(string="Mensaje")

	@api.multi
	def action_cerrar(self):
		return {'type': 'ir.actions.act_window_close'}