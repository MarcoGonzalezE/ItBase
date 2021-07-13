# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

class Compania(models.Model):
	_name = 'itbase.equipo.compania'

	name = fields.Char(string="Compañia")
	sequence = fields.Char(string="Inicio de Secuencia")
	imagen = fields.Binary(string="Logo", attachment=True)
	#EQUIPOS
	equipos_ids = fields.One2many('itbase.equipo','company_id', string="Equipos")
	equipos_cont = fields.Integer(compute='get_contadores')
	#SERVIDORES
	servidores_ids = fields.One2many('itbase.servidores', 'compania', string="Servidores")
	servidores_cont = fields.Integer(compute='get_contadores')
	#DISPOSITIVOS DE RED
	dispositivos_ids = fields.One2many('itbase.redes', 'company_id', string="Dispositivos")
	dispositivos_cont = fields.Integer(compute='get_contadores')
	#TELEFONOS
	telefonos_ids = fields.One2many('itbase.redes.telefonos', 'company_id', string="Telefonos")
	telefonos_cont = fields.Integer(compute='get_contadores')
	#PROYECTOS
	proyectos_ids = fields.One2many('itbase.proyectos', 'compania', string="Proyectos")
	proyectos_cont = fields.Integer(compute='get_contadores')
	productos_cont = fields.Integer(compute="get_contadores")
	#SOPORTES
	soportes_ids = fields.One2many('itbase.soporte', 'compania', string="Soportes")
	soporte_cont = fields.Integer(compute='get_contadores')
	#REUNIONES
	reuniones_ids = fields.One2many('itbase.reuniones', 'compania', string="Reuniones")
	reuniones_cont = fields.Integer(compute='get_contadores')
	#SECUENCIAS
	prefijo_escritorio = fields.Char(string="Inicio de secuencia escritorio")
	prefijo_laptop = fields.Char(string="Inicio de secuencia laptop")
	prefijo_celular = fields.Char(string="Inicio de secuencia celular")
	siguiente_escritorio = fields.Integer(string="N° proximo equipo de escritorio", default="1")
	siguiente_laptop = fields.Integer(string="N° proximo de laptop", default="1")
	siguiente_celular = fields.Integer(string="N° proximo celular", default="1")

	@api.onchange('sequence')
	def secuencias_compania(self):
		self.prefijo_laptop = self.sequence
		self.prefijo_celular = self.sequence
		self.prefijo_escritorio = self.sequence

	@api.one
	@api.depends('equipos_ids', 'servidores_ids', 'dispositivos_ids', 'telefonos_ids', 'proyectos_ids', 'soportes_ids', 'reuniones_ids')
	def get_contadores(self):
		self.equipos_cont = len(self.equipos_ids)
		self.servidores_cont = len(self.servidores_ids)
		self.dispositivos_cont = len(self.dispositivos_ids)
		self.telefonos_cont = len(self.telefonos_ids)
		self.proyectos_cont = len(self.proyectos_ids)
		self.productos_cont = len(self.env['itbase.productos'].search([('compania','=',self.id)]))
		self.soporte_cont = len(self.soportes_ids)
		self.reuniones_cont = len(self.reuniones_ids)
		
	@api.multi
	def act_equipos(self):
		action = self.env.ref('ItBase.itbase_computadora_action')
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_type': action.view_type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		result['domain'] = "[('id','in',["+','.join(map(str, self.equipos_ids.ids))+"])]"
		return result

	@api.multi
	def act_servidores(self):
		action = self.env.ref('ItBase.itbase_servidores_action')
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_type': action.view_type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		result['domain'] = "[('id','in',["+','.join(map(str, self.servidores_ids.ids))+"])]"
		return result

	@api.multi
	def act_dispositivos(self):
		action = self.env.ref('ItBase.itbase_redes_action')
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_type': action.view_type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		result['domain'] = "[('id','in',["+','.join(map(str, self.dispositivos_ids.ids))+"])]"
		return result

	@api.multi
	def act_telefonos(self):
		action = self.env.ref('ItBase.itbase_redes_telefonos_action')
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_type': action.view_type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		result['domain'] = "[('id','in',["+','.join(map(str, self.telefonos_ids.ids))+"])]"
		return result

	@api.multi
	def act_proyectos(self):
		action = self.env.ref('ItBase.itbase_proyectos_action')
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_type': action.view_type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		result['domain'] = "[('id','in',["+','.join(map(str, self.proyectos_ids.ids))+"])]"
		return result

	@api.multi
	def act_soportes(self):
		action = self.env.ref('ItBase.itbase_soporte_action')
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_type': action.view_type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		result['domain'] = "[('id','in',["+','.join(map(str, self.soportes_ids.ids))+"])]"
		return result

	@api.multi
	def act_reuniones(self):
		action = self.env.ref('ItBase.itbase_reuniones_action')
		result = {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_type': action.view_type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
		}
		result['domain'] = "[('id','in',["+','.join(map(str, self.reuniones_ids.ids))+"])]"
		return result