# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

class ItBase_Equipo(models.Model):
	_name = 'itbase.equipo'
	_inherit = ['mail.thread']

	name = fields.Char(default="Nuevo", store=True, track_visibility='onchange')
	marca = fields.Many2one('itbase.marca', string="Marca", track_visibility='onchange')
	modelo = fields.Char(string="Modelo", track_visibility='onchange')
	so_id = fields.Many2one('itbase.so', string="Sistema Operativo", track_visibility='onchange')
	procesador = fields.Char()
	ram = fields.Integer()
	numero_tel = fields.Char(string="Numero de Telefono")
	imei = fields.Char(string="IMEI")
	ip = fields.Char(string="IP")
	mac = fields.Char(string="MAC")
	telefonia = fields.Char(string="Compañia Telefonica")
	tipo = fields.Selection([('escritorio','Escritorio'),
							('laptop','Laptop'),
							('celular','Telefono/Celular')],
							string="Tipo", track_visibility='onchange')
	arquitectura = fields.Selection([('x_32','32 bits'),('x_64','64 bits')], string="Arquitectura")
	estado = fields.Selection([('created','Creado'),
								('not_assigned','Sin Asignar'),
								('assigned','Asignado'),
								('repair','Reparacion'),
								('maintenance','Mantenimiento'),
								('scrap','Desecho')],
								string = "Estado", default='created', track_visibility='onchange')
	imagen_variante = fields.Binary(attachment=True)
	imagen = fields.Binary(string="Imagen Computadora", attachment=True)
	imagen_small = fields.Binary(attachment=True)
	imagen_medium = fields.Binary(attachment=True)
	company_id = fields.Many2one('itbase.equipo.compania', string="Compañia")
	equipo_nuevo = fields.Boolean(string="Equipo Nuevo")

	_sql_constraints = [('equipo_uniq', 'UNIQUE (name)', '¡Numero de equipo ya existente!')]

	@api.one
	@api.depends('imagen_variante','imagen')
	def _compute_images(self):
		if self._context.get('bin_size'):
			self.imagen_medium = self.imagen_variante
		else:
			resized_images = tools.image_get_resized_images(self.imagen_variante, return_big=True, avoid_resize_medium=True)
			self.imagen_medium = resized_images['image_medium']
	@api.one
	def _set_image_medium(self):
		self._set_image_value(self.imagen_medium)

	@api.one
	def _set_image_value(self, value):
		image = tools.image_resize_image_big(value)
		if self.imagen:
			self.imagen_variante = image
		else:
			self.imagen = image

	@api.onchange('company_id','tipo')
	def _onchange_compania(self):
		if self.company_id:
			if self.tipo == 'escritorio':
				self.name = self.company_id.prefijo_escritorio + '%%0%sd' % 3 % self.company_id.siguiente_escritorio
			if self.tipo == 'laptop':
				self.name = self.company_id.prefijo_laptop + '%%0%sd' % 3 % self.company_id.siguiente_laptop
			if self.tipo == 'celular':
				self.name = self.company_id.prefijo_celular + '%%0%sd' % 3 % self.company_id.siguiente_celular
			
	@api.model
	def create(self, vals):
		nuevo = super(ItBase_Equipo, self).create(vals)
		if nuevo.tipo == 'escritorio':
			nuevo.company_id.siguiente_escritorio += 1
		if nuevo.tipo == 'laptop':
			nuevo.company_id.siguiente_laptop += 1
		if nuevo.tipo == 'celular':
			nuevo.company_id.siguiente_celular += 1
		nuevo.estado = 'not_assigned'
		return nuevo	

#CONTADOR DE MANTENIMIENTOS
	mantenimiento_ids = fields.One2many('itbase.mantenimiento', 'equipo_id', string="Mantenimientos")
	mantenimiento_cont = fields.Integer(compute="get_contadores")
	mantenimiento = fields.Char(compute="get_contadores", string="Mantenimientos Activos")

	@api.one
	@api.depends('mantenimiento')
	def get_contadores(self):
		self.mantenimiento_cont = len(self.mantenimiento_ids)
		self.mantenimiento = len(self.env['itbase.mantenimiento'].search([('equipo_id','=',self.id),('estado','!=','final'),('estado','!=','cancel')]))

	@api.multi
	def act_mantenimientos(self):
		action = self.env.ref('ItBase.itbase_mantenimiento_equipo_action')
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
		result['domain'] = "[('id','in',["+','.join(map(str, self.mantenimiento_ids.ids))+"])]"
		return result

#DISPOSITIVOS EXTRA
	dispositivos_ids = fields.One2many('itbase.dispositivo', 'equipo_id', string='Dispositivos')

#PROGRAMAS ADICIONALES - LICENCIAS
	licencia_ids = fields.One2many('itbase.licencia', 'equipo_id', string="Licencias")

#HISTORIAL DE ASIGNACIONES
	asignar_ids = fields.One2many('itbase.equipo.asignar', 'equipo_id', string="Asignaciones")

#ULTIMO ASIGNADO
	asignado = fields.Many2one('itbase.equipo.asignar', string="Asignada(o)", track_visibility='onchange')
	correo = fields.Char(related="asignado.correo", string="Correo", track_visibility='onchange')
	departamento = fields.Char(related="asignado.departamento", string="Departamento", track_visibility='onchange')
	fecha_asignacion = fields.Date(related="asignado.fecha_asignacion", string="Fecha de Asignacion", track_visibility='onchange')

	@api.multi
	def asignar_equipo(self):
		return {
            'name': "Asignar equipo",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_name': 'form',
            'res_model': 'itbase.equipo.transaccion',
            'context': {'default_equipo_id': self.id},
            'target': 'new'
        }

	@api.multi
	def disponible_equipo(self):
		form_id = self.env.ref('ItBase.itbase_devolucion_view_form')
		return {
            'name': "Devolucion de equipo",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'res_id': self.asignado.id,
            'view_id': form_id.id,
            'view_mode': 'form',
            'view_name': 'form',
            'res_model': 'itbase.equipo.asignar',
            'context': {},
            'target': 'new'
        }

	def reparacion_equipo(self):
		if self.estado == 'repair':
			if self.asignado:
				self.estado = 'assigned'
			else:
				self.estado = 'not_assigned'
		else:
			self.estado = 'repair'

	def mantenimiento_equipo(self):
		self.estado = 'maintenance'
		mantenimiento = self.env['itbase.mantenimiento'].create({
			'equipo_id': self.id,
			})
		return{
			'name': 'Mantenimiento',
            'view_id': self.env.ref('ItBase.itbase_mantenimiento_equipo_view_form').id,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'itbase.mantenimiento',
            'res_id': mantenimiento.id,
            'type': 'ir.actions.act_window'
		}

	def desecho_equipo(self):
		self.estado = 'scrap'

	@api.multi
	def name_get(self):
		res = super(ItBase_Equipo, self).name_get()
		result = []
		for element in res:
			equipo_id = element[0]
			code = self.browse(equipo_id).name
			desc = self.browse(equipo_id).asignado.nombre
			name = code and '[%s] %s' % (code, desc) or '%s' % desc
			result.append((equipo_id, name))
		return result

	def reporte_asignacion(self):
		return self.env['report'].get_action(self, 'ItBase.carta_responsiva_document')

	def reporte_devolucion(self):
		return self.env['report'].get_action(self, 'ItBase.carta_devolucion_document')

class SistemaOperativo(models.Model):
	_name = 'itbase.so'
	name = fields.Char(string="Sistema Operativo", required=True)

class Marca(models.Model):
	_name = "itbase.marca"
	name = fields.Char(string="Marca", required=True)

class ProgramaLicencia(models.Model):
	_name = 'itbase.licencia'
	equipo_id = fields.Many2one('itbase.equipo', string='ID Equipo')
	name = fields.Char(string="Programa")
	licencia_bolean = fields.Selection([('si','Si'),('no','No')], string='¿Licencia?')
	numero_licencia = fields.Char(string="Numero de Licencia")

class AsignacionesEquipos(models.TransientModel):
	_name = 'itbase.equipo.transaccion'

	equipo_id = fields.Many2one('itbase.equipo', string='Equipo')
	name = fields.Many2one('res.partner', string="Asignada(o)")
	nombre = fields.Char(string="Asignado(a) sin registro")
	correo = fields.Char(string="Correo")
	departamento = fields.Char(string="Departamento")
	fecha_asignacion = fields.Date(string="Fecha de Asignacion")
	fecha_devolucion = fields.Date(string="Fecha de Devolucion")
	nota = fields.Char(string="Nota")

	@api.onchange('name')
	def _onchange_asignado(self):
		self.nombre = self.name.name
		self.correo = self.name.email

	@api.multi
	def asignar(self):
		equipo = self.env['itbase.equipo'].browse(self._context.get('active_ids'))
		asignaciones = self.env['itbase.equipo.asignar'].create({
			'equipo_id': self.equipo_id.id,
			'nombre': self.nombre,
			'correo': self.correo,
			'departamento': self.departamento,
			'fecha_asignacion': self.fecha_asignacion,
			'nota': self.nota
			})
		equipo.asignado = asignaciones.id
		equipo.estado = 'assigned'
		return True

class AsignacionEquipo(models.Model):
	_name =	'itbase.equipo.asignar'
	_rec_name = 'nombre'
	
	equipo_id = fields.Many2one('itbase.equipo', string='Equipo')
	name = fields.Many2one('res.partner', string="Asignada(o)")
	nombre = fields.Char(string="Asignado(a)")
	correo = fields.Char(string="Correo")
	departamento = fields.Char(string="Departamento")
	fecha_asignacion = fields.Date(string="Fecha de Asignacion")
	fecha_devolucion = fields.Date(string="Fecha de Devolucion")
	nota = fields.Char(string="Nota")

	def reporte_devolucion(self):
		reporte = self.equipo_id.reporte_devolucion()
		return reporte

	def devolucion(self):
		self.equipo_id.estado = 'not_assigned'
		self.equipo_id.asignado = False
		self.equipo_id.correo = False
		self.equipo_id.departamento = False
		self.equipo_id.fecha_asignacion = False
		return True