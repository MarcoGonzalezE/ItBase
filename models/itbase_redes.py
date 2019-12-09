# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

class ItBaseRedes(models.Model):
	_name = 'itbase.redes'	
	_inherit = ['mail.thread']

	name = fields.Char(string="Nombre", track_visibility='onchange')
	modelo = fields.Char(string="Modelo", track_visibility='onchange')
	marca = fields.Many2one('itbase.marca', string="Marca", track_visibility='onchange')
	tipo = fields.Many2one('itbase.redes.dispositivo', string="Tipo", track_visibility='onchange')
	ip = fields.Char(string="IP", track_visibility='onchange')
	company_id = fields.Many2one('itbase.equipo.compania', string="Compañia")
	usuario = fields.Char(string="Usuario", track_visibility='onchange')
	contrasena = fields.Char(string="Contrasena", track_visibility='onchange')
	proveedor = fields.Many2one('res.partner', string="Proveedor", track_visibility='onchange')
	ubicacion = fields.Char(string="Ubicacion")
	imagen = fields.Binary(string="Avatar", attachment=True)

class TipoDispositivo(models.Model):
	_name = 'itbase.redes.dispositivo'
	name = fields.Char(string="Dispositivo Tipo", required=True)

class RedesTelefonos(models.Model):
	_name = 'itbase.redes.telefonos'

	name = fields.Char(string='Numero')
	company_id = fields.Many2one('itbase.equipo.compania', string="Compañia")
	telefonia = fields.Char(string="Compañia Telefonica")
	conmutador = fields.Many2one('itbase.redes', string="Conmutador")
	reportes_id = fields.One2many('itbase.redes.telefonos.resportes', 'telefono_id', string="Reportes")

	@api.onchange('conmutador')
	def _onchange_compania(self):
		self.company_id = self.conmutador.company_id

class RedesTelefonosReportes(models.Model):
	_name = 'itbase.redes.telefonos.resportes'

	telefono_id = fields.Many2one('itbase.redes.telefonos', string="Telefono ID")
	fecha_inicio = fields.Date(string="Fecha de Falla")
	fecha_final = fields.Date(string="Fecha de Restablecimiento")
	reporte = fields.Char(string="Reporte")



