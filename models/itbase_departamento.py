from odoo import api, fields, models, _
from odoo.exceptions import Warning
import datetime
from odoo import SUPERUSER_ID

class ItBaseDepartamento(models.Model):
	_name = 'itbase.departamento'

	name = fields.Many2one('res.users', string="Nombre")
	puesto = fields.Char(string="Puesto")
	correo = fields.Char(string="Correo")
	telefono = fields.Char(string="Telefono")
	imagen = fields.Binary(string="Avatar", attachment=True)
	activo = fields.Boolean('Activo', default=True)
	notificaciones = fields.Many2many('itbase.notificaciones.medios', string="Notificaciones")
	#MANTENIMIENTOS
	mantenimientos_ids = fields.One2many('itbase.mantenimiento', 'encargado', string="Mantenimientos")
	mantenimientos_count = fields.Integer(compute='get_contadores')
	#SOPORTES
	soportes_ids = fields.One2many('itbase.soporte', 'asignada', string="Soporte")
	soportes_count = fields.Integer(compute='get_contadores')
	#TAREAS
	tareas_ids = fields.One2many('itbase.proyectos.tarea', 'responsable', string="Tareas")
	tareas_count = fields.Integer(compute='get_contadores')
	bugs_count = fields.Integer(compute='get_contadores')
	#SERVIDORES
	servidores_ids = fields.One2many('itbase.servidores', 'responsable', string="Servidores")
	servidores_count = fields.Integer(compute='get_contadores')
	#PRODUCTOS
	productos_ids = fields.One2many('itbase.productos', 'responsable', string="Productos")
	productos_count = fields.Integer(compute='get_contadores')
	#HISTORIAS
	historias_ids = fields.One2many('itbase.historias', 'responsable', string="Historias")
	historias_count = fields.Integer(compute='get_contadores')

	@api.multi
	def estado_activo(self):
		for r in self:
			r.activo = not r.activo

	@api.one
	@api.depends('mantenimientos_ids','soportes_ids','tareas_ids','servidores_ids','productos_ids','historias_ids')
	def get_contadores(self):
		self.mantenimientos_count = len(self.mantenimientos_ids)
		self.soportes_count = len(self.soportes_ids)
		self.tareas_count = len(self.tareas_ids)
		self.bugs_count = len(self.env['itbase.errores'].search([('responsable','=',self.id)]))
		self.servidores_count = len(self.servidores_ids)
		self.productos_count = len(self.productos_ids)
		self.historias_count = len(self.historias_ids)

	@api.multi
	def act_mantenimientos(self):
		action = self.env.ref('ItBase.itbase_mantenimientos_action')
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
		result['domain'] = "[('id','in',["+','.join(map(str, self.mantenimientos_ids.ids))+"])]"
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
	def act_tareas(self):
		action = self.env.ref('ItBase.itbase_tareas_action')
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
		result['domain'] = "[('id','in',["+','.join(map(str, self.tareas_ids.ids))+"])]"
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
	def act_productos(self):
		action = self.env.ref('ItBase.itbase_productos_action')
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
		result['domain'] = "[('id','in',["+','.join(map(str, self.productos_ids.ids))+"])]"
		return result

	@api.multi
	def act_historias(self):
		action = self.env.ref('ItBase.itbase_historias_action')
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
		result['domain'] = "[('id','in',["+','.join(map(str, self.historias_ids.ids))+"])]"
		return result

class ITBaseNotificacionesMedios(models.Model):
	_name = 'itbase.notificaciones.medios'
	_description = "Medios de notificaciones"
	_rec_name = "nombre"

	nombre = fields.Char(string="Medio")
