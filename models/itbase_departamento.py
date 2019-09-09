from odoo import api, fields, models, _
from odoo.exceptions import Warning
import datetime
from odoo import SUPERUSER_ID

class ItBaseDepartamento(models.Model):
	_name = 'itbase.departamento'

	name = fields.Many2one('res.users', string="Nombre")
	puesto = fields.Char(string="Puesto")
	imagen = fields.Binary(string="Avatar", attachment=True)

#CONTADOR DE MANTENIMIENTOS REALIZADOS
	mantenimiento = fields.One2many('itbase.mantenimiento', 'encargado', string="Mantenimientos")
	mantenimiento_count = fields.Integer(compute="_count_mantenimiento", string="Mantenimientos")
	mantenimientos = fields.Char(compute="_count_mantenimientos", string="Mantenimientos")

	@api.one
	@api.depends('mantenimiento')
	def _count_mantenimiento(self):
		self.mantenimiento_count = self.mantenimiento.search_count([('encargado','=',self.id)])

	@api.one
	@api.depends('mantenimiento_count')
	def _count_mantenimientos(self):
		self.mantenimientos = str(self.mantenimiento_count)

#CONTADOR DE SOPORTE REALIZADO
	soporte = fields.One2many('itbase.soporte', 'asignada', string="Soporte")
	soporte_count = fields.Integer(compute="_count_soporte", string="Soporte")
	soportes = fields.Char(compute="_count_soportes", string="Soporte")

	@api.one
	@api.depends('soporte')
	def _count_soporte(self):
		self.soporte_count = self.soporte.search_count([('asignada','=',self.id)])

	@api.one
	@api.depends('soporte_count')
	def _count_soportes(self):
		self.soportes = str(self.soporte_count)