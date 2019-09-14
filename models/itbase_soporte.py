# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

PRIORIDADES = [('0', 'Muy bajo'), ('1', 'Bajo'), ('2', 'Normal'), ('3', 'Alto'), ('4', 'Muy alto')]

class ItBaseSoporte(models.Model):
	_name = 'itbase.soporte'
	_inherit = ['mail.thread']

	def _default_fecha_soporte(self):
		return datetime.datetime.now()

	name = fields.Char(string="Asunto", track_visibility='onchange')
	solicitante = fields.Many2one('res.partner', string="Solicitante")
	correo = fields.Char(string="Correo")
	asignada = fields.Many2one('itbase.departamento', string="Asignada", track_visibility='onchange')
	prioridad = fields.Selection(PRIORIDADES, select=True, string="Prioridad", default=PRIORIDADES[0][0], track_visibility='onchange')
	fecha_soporte = fields.Datetime(string="Fecha de solicitud", default=_default_fecha_soporte, track_visibility='onchange')
	fecha_limite = fields.Date(string="Fecha limite", track_visibility='onchange')
	fecha_fin = fields.Datetime(string="Fecha finalizacion", track_visibility='onchange')
	descripcion = fields.Char(string="Descripcion")
	estado = fields.Selection([('nuevo','Nuevo'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('cancel','Cancelado')], string="Estado", default='nuevo', track_visibility='onchange')
	equipo_id = fields.Many2one('itbase.equipo', string="Equipo", track_visibility='onchange')

	@api.onchange('solicitante')
	def _onchange_solicitante(self):
		self.correo = self.solicitante.email

	@api.onchange('estado')
	def _onchange_estado(self):
		if self.estado == 'Completado':
			self.fecha_fin = datetime.datetime.now()

	def cancelar(self):
		self.estado = 'cancel'

	#@api.model
	#def create(self, vals):
	 	# self.fecha_soporte = datetime.datetime.now()

	
		