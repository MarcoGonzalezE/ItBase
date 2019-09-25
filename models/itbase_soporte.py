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
	seq = fields.Char(string="Secuencia", store="True")
	solicitante = fields.Many2one('res.partner', string="Solicitante")
	correo = fields.Char(string="Correo")
	asignada = fields.Many2one('itbase.departamento', string="Asignada", track_visibility='onchange')
	prioridad = fields.Selection(PRIORIDADES, select=True, string="Prioridad", default=PRIORIDADES[0][0], track_visibility='onchange')
	fecha_soporte = fields.Datetime(string="Fecha de solicitud", default=_default_fecha_soporte, track_visibility='onchange')
	fecha_limite = fields.Date(string="Fecha limite", track_visibility='onchange')
	fecha_fin = fields.Datetime(string="Fecha finalizacion", compute="_compute_fechafin", track_visibility='onchange')
	descripcion = fields.Char(string="Descripcion")
	estado = fields.Selection([('nuevo','Nuevo'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('cancel','Cancelado')], string="Estado", default='nuevo', track_visibility='onchange')
	equipo_id = fields.Many2one('itbase.equipo', string="Equipo", track_visibility='onchange')
	producto_id = fields.Many2one('itbase.productos', string="Producto", track_visibility='onchange')
	proyecto_id = fields.Many2one('itbase.proyectos', string="Proyecto", track_visibility='onchange')

	@api.onchange('solicitante')
	def _onchange_solicitante(self):
		self.correo = self.solicitante.email

	@api.onchange('producto_id')
	def _onchange_producto(self):
		self.proyecto_id = self.producto_id.proyecto
		pass

	@api.depends('estado')
	def _compute_fechafin(self):
		if self.estado == 'complete':
			self.fecha_fin = datetime.datetime.now()

	def cancelar(self):
		self.estado = 'cancel'

	@api.model
	def create(self, vals):
		if vals.get('seq', "Nuevo") == "Nuevo":
			vals['seq'] = self.env['ir.sequence'].next_by_code('itbase.soporte') or "Nuevo"
			return super(ItBaseSoporte, self).create(vals)

	@api.multi
	def name_get(self):
		res = super(ItBaseSoporte, self).name_get()
		result = []
		for element in res:
			soporte_id = element[0]
			code = self.browse(soporte_id).seq
			desc = self.browse(soporte_id).name
			name = code and '[%s] %s' % (code, desc) or '%s' % desc
			result.append((soporte_id, name))
		return result		