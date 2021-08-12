# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import json
import requests

class ItBaseConfiguracion(models.TransientModel):
	_name = 'itbase.config.settings'
	_inherit = 'res.config.settings'

	#TELEGRAM
	activar_telegram = fields.Boolean(string="Usar Telegram")
	token_telegram = fields.Char(string="Token")
	id_chat = fields.Char(string="ID Chat")
	conexiones_ids = fields.One2many('itbase.config.settings.telegram.line', 'line_id', string="Conexiones")
	#RECORDATORIOS
	correo_recordatorios = fields.Boolean(string="Notificar por Correo")
	telegram_recordatorios = fields.Boolean(string="Notificar por Telegram")
	# usar_intervalo = fields.Boolean(string="Notificar antes")
	# intervalo = fields.Integer(string="Numero")
	# intervalo_tipo = fields.Selection([('minutes','Minutos'),('hours','Horas'),('days','Dias')], string="Unidad")
	# semanal_recordatorios = fields.Boolean(string="Recordatorios totales semanal")

	@api.onchange('activar_telegram')
	def onchange_telegram(self):
		if self.activar_telegram == False:
			self.token_telegram = False
			self.id_chat = False
			self.conexiones_ids.unlink()

	def comprobarTelegram(self, token):
		comprobacion = "https://api.telegram.org/bot" + token + "/getUpdates"
		respuesta = requests.get(comprobacion)
		return respuesta.json()

	def btVerificarTelegram(self):
		self.conexiones_ids.unlink()
		mensaje = ""
		conectado = False
		conexiones = []
		resultado = []
		verificar = self.comprobarTelegram(self.token_telegram)
		if verificar["ok"] == True:
			mensaje = "¡Telegram Bot funcionando correctamente!"			
			conectado = True
			result = verificar['result']
			message = {}
			for r in result:
				try:
					message = r['message']
					chat = message['chat']
					try:
						nombre = (chat['first_name']) + ' ' + (chat['last_name'])
						conexiones.append([(chat['id']), nombre, 'Usuario'])
					except:
						conexiones.append([(chat['id']), (chat['first_name']), 'Usuario'])
				except:
					pass
				try:
					message = r['my_chat_member']
					chat = message['chat']
					conexiones.append([(chat['id']), (chat['title']), 'Grupo'])
				except:
					pass
			conexiones.sort()
			if conexiones:
				flag = conexiones[0][0]
				resultado.append((0,0,{'id_conexion':conexiones[0][0],'nombre':conexiones[0][1],'tipo':conexiones[0][2],'line_id':self.id}))
				for c in conexiones:
					if c[0] != flag:
						resultado.append((0,0,{'id_conexion':c[0],'nombre':c[1],'tipo':c[2],'line_id':self.id}))
						flag = c[0]
				self.conexiones_ids = resultado
			else:
				mensaje += "\nPero sin conversaciones activas."
		else:
			mensaje = "Verifique su conexion internet o Token"
			conectado = False
		mensaje_id = self.env['itbase.mensaje.wizard'].create({'mensaje':_(mensaje)})
		return {
			'name': _("Conexion Telegram"),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'itbase.mensaje.wizard',
			'res_id': mensaje_id.id,
			'target': 'new'
		}

class ItBaseConfiguracionTelegramLineas(models.TransientModel):
	_name = 'itbase.config.settings.telegram.line'

	line_id = fields.Many2one('itbase.config.settings', string="Conexion")
	id_conexion = fields.Char(string="ID")
	nombre = fields.Char(string="Nombre")
	tipo = fields.Char(string="Tipo")
	principal = fields.Boolean(string="Principal")
	asignar_id = fields.Many2one('itbase.departamento', string="Asignar a Usuario")

	def btUsarPrincipal(self):
		conexiones = self.env['itbase.config.settings.telegram.line'].search([])
		for c in conexiones:
			c.principal = False
		self.principal = True
		self.line_id.id_chat = self.id_conexion

	def fnAbrirConexion(self):
		form_id = self.env.ref('ItBase.itbase_asignacion_telegram_form')
		return {
			'name': "Asignar ID de Chat",
			'type': 'ir.actions.act_window',
			'view_type': 'form',
            'res_id': self.id,
            'view_id': form_id.id,
            'view_mode': 'form',
            'view_name': 'form',
            'res_model': 'itbase.config.settings.telegram.line',
            'context': {},
            'target': 'new'
		}

	def btAsignarID(self):
		self.asignar_id.id_telegram = self.id_conexion
		return True
