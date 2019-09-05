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
