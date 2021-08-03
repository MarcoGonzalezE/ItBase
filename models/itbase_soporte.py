# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime
from odoo.exceptions import ValidationError
import requests


PRIORIDADES = [('0', 'Muy bajo'), ('1', 'Bajo'), ('2', 'Normal'), ('3', 'Alto'), ('4', 'Muy alto')]

class ItBaseSoporte(models.Model):
	_name = 'itbase.soporte'
	_rec_name = 'seq'
	_inherit = ['mail.thread']

	def _default_fecha_soporte(self):
		return datetime.datetime.now()

	name = fields.Char(string="Asunto", track_visibility='onchange')
	seq = fields.Char(string="Secuencia", store=True)
	solicitante = fields.Many2one('res.partner', string="Solicitante")
	solicitante_id = fields.Char(string="solicitante")
	correo = fields.Char(string="Correo")
	asignada = fields.Many2one('itbase.departamento', string="Asignada", track_visibility='onchange')
	prioridad = fields.Selection(PRIORIDADES, select=True, string="Prioridad", default=PRIORIDADES[0][0], track_visibility='onchange')
	fecha_soporte = fields.Datetime(string="Fecha de solicitud", default=_default_fecha_soporte, track_visibility='onchange')
	fecha_limite = fields.Date(string="Fecha limite", track_visibility='onchange')
	fecha_fin = fields.Datetime(string="Fecha finalizacion", track_visibility='onchange', store=True, compute="_get_fechafin")
	descripcion = fields.Char(string="Descripcion")
	estado = fields.Selection([('nuevo','Nuevo'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('cancel','Cancelado')], string="Estado", default='nuevo', track_visibility='onchange')
	equipo_id = fields.Many2one('itbase.equipo', string="Equipo", track_visibility='onchange')
	producto_id = fields.Many2one('itbase.productos', string="Producto", track_visibility='onchange')
	proyecto_id = fields.Many2one('itbase.proyectos', string="Proyecto", track_visibility='onchange')
	compania = fields.Many2one('itbase.equipo.compania', string="Compania", track_visibility='onchange')
	tarea_id = fields.Many2one('itbase.proyectos.tarea', string="Tarea", track_visibility='onchange')

	@api.onchange('solicitante')
	def _onchange_solicitante(self):
		self.solicitante_id = self.solicitante.name
		self.correo = self.solicitante.email

	@api.onchange('producto_id')
	def _onchange_producto(self):
		self.proyecto_id = self.producto_id.proyecto	

	def cancelar(self):
		self.estado = 'cancel'

	def notificacion_telegram(self, mensaje, url):
		bot_mensaje = mensaje + '\n' + url
		print bot_mensaje
		parametro = self.env['itbase.config.settings'].search([])
		token = parametro.token_telegram
		chatID = parametro.id_chat
		enviar_mensaje = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chatID + "&parse_mode=HTML&text=" + mensaje #+ "&reply_markup='inline_keyboard':[{'text':'VER SOLICITUD','url': 'http://odoo.avicampo.com.mx/support/help',}]"
		respuesta = requests.get(enviar_mensaje)
		return respuesta.json()

	@api.model
	def create(self, vals):
		if vals.get('seq', "Nuevo") == "Nuevo":
			vals['seq'] = self.env['ir.sequence'].next_by_code('itbase.soporte') or "Nuevo"
		nuevo = super(ItBaseSoporte, self).create(vals)
		personal_it = self.env['itbase.departamento'].search([('activo','=',"true")])
		if nuevo.asignada:
			print("")
		else:
			#CORREO
			notificacion_soporte = self.env['ir.model.data'].sudo().get_object('ItBase','itbase_soporte_ticket_nuevo')
			menu_soporte = self.env['ir.model.data'].sudo().get_object('ItBase','itbase_soporte_menu')
			action_soporte = self.env['ir.model.data'].sudo().get_object('ItBase','itbase_soporte_action')
			for it in personal_it:
				if it.correo:
					print ("Tiene Correo")
					if it.notificaciones.nombre == "Correo":
						print  ("Correo Enviado")
						values = notificacion_soporte.generate_email(nuevo.id)
						values['body_html'] = values['body_html'].replace("_ticket_url_", "web#id=" +
								str(nuevo.id) + "&view_type=form&model=itbase.soporte&menu_id=" +
								str(menu_soporte.id) + "&action=" + str(action_soporte.id)).replace("_personal_it", it.name.name)
						values['email_to'] = it.correo
						send_mail = self.env['mail.mail'].create(values)
						send_mail.send()
			notificacion = "Se ha creado una nueva solicitud de Soporte\nFolio: " + str(nuevo.seq) + "\nEmpresa: " + str(nuevo.compania.name) + "\nFecha de Solicitud: " + str(nuevo.fecha_soporte) + "\nSolicitante: " + str(nuevo.solicitante_id) + "\nEquipo: " + str(nuevo.equipo_id.name) + "\nAsunto: " + str(nuevo.name) + "\nDescripcion: " + str(nuevo.descripcion)
			url = "<a href=web#id=" + str(nuevo.id) + '&view_type=form&model=itbase.soporte&menu_id=' + str(menu_soporte.id) + '&action=' + str(action_soporte.id) + ">VER SOLICITUD</a>"
			#TELEGRAM
			print (notificacion, url)
			nuevo.notificacion_telegram(notificacion, url)
		return nuevo
	@api.depends('estado')
	def _get_fechafin(self):
		if self.estado == 'complete':
			self.fecha_fin = datetime.datetime.now()

	# @api.multi
	# def write(self, values):
	# 	if self.estado == 'complete':
	# 		self.fecha_fin = datetime.datetime.now()

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

class SoporteTareas(models.TransientModel):
	_name = 'itbase.soporte.tarea'

	# @api.model
	# def default_get(self, default_fields):
	# 	res = super(SoporteTareas, self).default_get(default_fields)
	# 	soporte_ids = self._context.get('active_ids')
	# 	soportes = self.env['itbase.soporte'].browse(soporte_ids)
	# 	return res

	@api.multi
	def crear_tarea(self):
		soportes = self.env['itbase.soporte'].browse(self._context.get('active_ids'))
		tarea_id = self.env['itbase.proyectos.tarea'].create({
			'proyecto_id': soportes[0].proyecto_id.id,
			'name': soportes[0].name,
			'responsable': soportes[0].asignada.id,
			'soporte_id': soportes[0].id
			})
		for record in soportes:
			record.write({'tarea_id': tarea_id.id})
			record.write({'estado':'cancel'})
			tarea_id.write({'soporte_ids':[(4, record.id)]})
		message = ('<strong>Se cambio a tarea:</strong> %s </br>') % (', '.join(soportes.mapped('name')))
		tarea_id.message_post(body=message)
		return{
			'name': 'Tareas',
			'view_id': self.env.ref('ItBase.itbase_tareas_form_view').id,
			'view_type':'form',
			'view_mode':'form',
			'res_model':'itbase.proyectos.tarea',
			'res_id':tarea_id.id,
			'type':'ir.actions.act_window'
		}