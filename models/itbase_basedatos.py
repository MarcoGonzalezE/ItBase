from odoo import api, fields, models, _
from odoo.exceptions import Warning
import datetime
from odoo import SUPERUSER_ID

class ItBaseBaseDeDatos(models.Model):
	_name = 'itbase.basedatos'
	_inherit = ['mail.thread']

	name = fields.Char(string="Nombre")
	servidor_id = fields.Many2one('itbase.servidores', string="Servidor")
	ip = fields.Char(string="IP", compute="_get_server_data", store=True)
	contrasena = fields.Char(string="Contrasena")
	usuarios_ids = fields.One2many('itbase.basedatos.usuarios', 'base_id', string="Usuarios", track_visibility='onchange')
	sistema = fields.Many2one('itbase.basedatos.sistema', string="Gestor")
	puerto = fields.Char(string="Puerto")

	api.one
	@api.depends('servidor_id')
	def _get_server_data(self):
		if self.servidor_id:
			self.ip = self.servidor_id.ip

	#CONTADOR DE MANTENIMIENTOS
	mantenimiento = fields.One2many('itbase.mantenimiento', 'base_id', string="Mantenimientos")
	mantenimiento_count = fields.Integer(compute="_count_mantenimiento", string="Mantenimientos")
	mantenimientos = fields.Char(compute="_count_mantenimientos", string="Mantenimientos")

	@api.one
	@api.depends('mantenimiento')
	def _count_mantenimiento(self):
		self.mantenimiento_count = self.mantenimiento.search_count([('base_id','=',self.id)])

	@api.one
	@api.depends('mantenimiento_count')
	def _count_mantenimientos(self):
		self.mantenimientos = str(self.mantenimiento_count)

class ItBaseBaseDeDatosSistema(models.Model):
	_name = 'itbase.basedatos.sistema'
	name = fields.Char(string="Gestor")

class ItBaseBaseDeDatosUsuarios(models.Model):
	_name = 'itbase.basedatos.usuarios'

	base_id = fields.Many2one('itbase.basedatos', string="ID Base")
	name = fields.Char(string="Usuario")
	contrasena = fields.Char(string="Contrasena")

		
