from odoo import api, fields, models, _
from odoo.exceptions import Warning
import datetime
from odoo import SUPERUSER_ID

class ItBaseServidores(models.Model):
	_name = 'itbase.servidores'
	_inherit = ['mail.thread']

	name = fields.Char(string="Nombre", required=True, track_visibility='onchange')
	ip = fields.Char(string="IP", track_visibility='onchange')
	ip_tipo = fields.Selection([('public','DHCP'), ('static', 'ESTATICA')], 
                               string="Tipo", default=lambda *a: 'public')
	usuario = fields.Char(string="Usuario", track_visibility='onchange')
	contrasena = fields.Char(string="Contrasena", track_visibility='onchange')
	ssh = fields.Char(string="SSH", compute="_make_ssh_command")
	sistema = fields.Many2one('itbase.so', string="Sistema operativo")
	ram = fields.Integer()
	tipo = fields.Many2one('itbase.servidores.tipo', string="Tipo de Servidor")
	servicios_ids = fields.One2many('itbase.servidores.programas','servidor_id', string="Servicios", track_visibility='onchange')
	usuarios_ids = fields.Many2many('res.users', 'server_user_rel', 'server_id', 'user_id', string="Usuarios", track_visibility='onchange')
	proveedor = fields.Many2one('res.partner', string="Proveedor", track_visibility='onchange')
	estado = fields.Selection([('activo','Activo'),
								('inactivo','Inactivo')], string="Estado", track_visibility='onchange')
	compania = fields.Many2one('itbase.equipo.compania', string="Compania", track_visibility='onchange')

	@api.one
	@api.depends('ip', 'usuario')
	def _make_ssh_command(self):
		if self.ip and self.usuario:
			self.ssh = self.usuario + '@' + self.ip
		else:
			self.ssh = False

	@api.model
	def _default_user_id(self):
		return [self.env.context.get('uid'), SUPERUSER_ID]

#CONTADOR DE MANTENIMIENTOS
	mantenimiento = fields.One2many('itbase.mantenimiento', 'servidor_id', string="Mantenimientos")
	mantenimiento_count = fields.Integer(compute="_count_mantenimiento", string="Mantenimientos")
	mantenimientos = fields.Char(compute="_count_mantenimientos", string="Mantenimientos")

	@api.one
	@api.depends('mantenimiento')
	def _count_mantenimiento(self):
		self.mantenimiento_count = self.mantenimiento.search_count([('servidor_id','=',self.id)])

	@api.one
	@api.depends('mantenimiento_count')
	def _count_mantenimientos(self):
		self.mantenimientos = str(self.mantenimiento_count)

#CONTADOR DE BASE DE DATOS
	base = fields.One2many('itbase.basedatos', 'servidor_id', string="Bases")
	base_count = fields.Integer(compute="_count_base", string="Bases")
	bases = fields.Char(compute="_count_bases", string="Bases")

	@api.one
	@api.depends('base')
	def _count_base(self):
		self.base_count = self.base.search_count([('servidor_id','=',self.id)])

	@api.one
	@api.depends('base_count')
	def _count_bases(self):
		self.bases = str(self.base_count)


class ServidorTipo(models.Model):
	_name = 'itbase.servidores.tipo'
	name = fields.Char(string="Tipo de Servidor", required=True)

class ServidoresProgramas(models.Model):
	_name = 'itbase.servidores.programas'
	
	servidor_id = fields.Many2one('itbase.servidores', string='ID Servidor')
	name = fields.Char(string="Servicio")
	version = fields.Char(string="Version")
	usuario = fields.Char(string="Usuario")
	contrasena = fields.Char(string="Contrasena")
