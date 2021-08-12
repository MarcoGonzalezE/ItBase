# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime
from datetime import timedelta
import requests

class ItBaseRecordatorios(models.Model):
	_name = 'itbase.recordatorios'
	_description = "Recordatorios"

	name = fields.Char(string="Asunto")
	descripcion = fields.Text(string="Descripcion")
	fecha = fields.Datetime(string="Fecha", default=datetime.datetime.now())
	responsable = fields.Many2one('itbase.departamento', string="Responsable")
	estado = fields.Selection([('activo','Activo'),('finalizado','Finalizado'),('cancelado','Cancelado')], default='activo', string="Estado")

	@api.multi
	def notificar_recordatorio(self):
		notificacion_template = self.env['ir.model.data'].sudo().get_object('ItBase','itbase_recordatorio_notificacion')
		recordatorios = self.env['itbase.recordatorios'].sudo().search([('estado','=','activo')])
		configuracion = self.env['itbase.config.settings'].search([])
		#siguiente = False
		#Fecha Actual
		hoy = datetime.datetime.utcnow()
		fecha = (datetime.datetime.strptime(str(hoy),'%Y-%m-%d %H:%M:%S.%f')).strftime("%Y-%m-%d %H:%M")
		#Fecha antes de Recordatorio
		# if configuracion.usar_intervalo == True:
		# 	intervalo = configuracion.intervalo
		# 	if configuracion.intervalo_tipo == 'minutes':
		# 		antes = hoy + timedelta(minutes=intervalo)
		# 	if configuracion.intervalo_tipo == 'hours':
		# 		antes = hoy + timedelta(hours=intervalo)
		# 	if configuracion.intervalo_tipo == 'days':
		# 		antes = hoy + timedelta(days=intervalo)
		# 	fecha_antes = (datetime.datetime.strptime(str(antes),'%Y-%m-%d %H:%M:%S.%f')).strftime("%Y-%m-%d %H:%M")
		for r in recordatorios:
			# if configuracion.usar_intervalo == True:
			# 	if r.fecha == fecha_antes:
			# 		siguiente = True
			# else:
			# 	if fecha == r.fecha:
			# 		siguiente = True
			# 	else:
			# 		r.estado = 'finalizado'
			# if siguiente == True:
			if fecha == (datetime.datetime.strptime(str(r.fecha),'%Y-%m-%d %H:%M:%S')).strftime("%Y-%m-%d %H:%M"):
				for n in r.responsable.notificaciones:
					if configuracion.correo_recordatorios == True:
						if n.nombre == "Correo":
							if r.responsable.correo:
								values = notificacion_template.generate_email(r.id)
								values['email_to'] = r.responsable.correo
								send_mail = self.env['mail.mail'].create(values)
								send_mail.send()
					if n.nombre == "Telegram":
						if r.responsable.id_telegram:
							mensaje = "Recordatorio\nAsunto: " + str(r.name) + "\nFecha: " + str(r.fecha) + "\nResponsable: " + str(r.responsable.name.name) + "\nDescripcion: " + str(r.descripcion)
							r.notificacion_telegram(mensaje,r.responsable.id_telegram)
				#	siguiente = False
			if fecha > (datetime.datetime.strptime(str(r.fecha), '%Y-%m-%d %H:%M:%S')).strftime("%Y-%m-%d %H:%M"):
				r.estado = 'finalizado'
		#	print ("EJECUTANDOSE FUNCION DE RECORDATORIOS A LAS ", (datetime.datetime.strptime(str((hoy - timedelta(hours=6))),'%Y-%m-%d %H:%M:%S.%f')).strftime("%Y-%m-%d %H:%M"))

	# @api.multi
	# def recordatorio_semanal(self):
	# 	recordatorios = self.env['itbase.recordatorios'].sudo().search([('estado', '=', 'activo')], order="responsable asc")
	# 	personal_it = self.env['itbase.departamento'].search([])
	# 	configuracion = self.env['itbase.config.settings'].search([])
	# 	# Fecha Actual
	# 	hoy = datetime.datetime.utcnow()
	# 	fecha = (datetime.datetime.strptime(str(hoy), '%Y-%m-%d %H:%M:%S.%f')).strftime("%Y-%m-%d %H:%M:%S")
	# 	# Fecha a 7 dias
	# 	fecha_7dias = (datetime.datetime.strptime(str(hoy + timedelta(days=7)), '%Y-%m-%d %H:%M:%S.%f')).strftime("%Y-%m-%d %H:%M:%S")
	# 	cont = 0
	# 	mensaje = ""
	# 	if configuracion.semanal_recordatorios == True:
	# 		for r in recordatorios:
	# 			if fecha_7dias > r.fecha:
	# 				if r.fecha > fecha:
	# 					for it in personal_it:
	# 						if r.responsable == it.id:
	# 							cont += 1
	# 							mensaje = "\n" + str(cont) + ".- " + str(r.name) + " [" + str(r.fecha) + "]" + mensaje
	# 						if it.notificaciones.nombre == "Telegram":
	# 					for n in r.responsable.notificaciones:
	# 						if n.nombre == "Telegram":
	# 							if r.responsable.id_telegram:
	# 								mensaje = "Recordatorio\nAsunto: " + str(r.name) + "\nFecha: " + str(r.fecha) + "\nResponsable: " + str(r.responsable.name.name) + "\nDescripcion: " + str(r.descripcion)
	# 								r.notificacion_telegram(mensaje,r.responsable.id_telegram)

	def notificacion_telegram(self, mensaje, chatID):
		bot_mensaje = mensaje
		parametro = self.env['itbase.config.settings'].search([])
		token = parametro.token_telegram
		enviar_mensaje = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chatID + "&parse_mode=HTML&text=" + bot_mensaje
		respuesta = requests.get(enviar_mensaje)
		return respuesta.json()

	def cancelado(self):
		self.estado = 'cancelado'