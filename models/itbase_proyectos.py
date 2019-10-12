# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

PRIORIDADES = [('0', 'Muy bajo'), ('1', 'Bajo'), ('2', 'Normal'), ('3', 'Alto'), ('4', 'Muy alto')]

class ItBaseProyectos(models.Model):
	_name = 'itbase.proyectos'

	name = fields.Char(string="Nombre del Proyecto")
	compania = fields.Many2one('itbase.equipo.compania', string="Compania")
	fecha_inicio = fields.Date(string="Fecha de Inicio")
	fecha_fin = fields.Date(string="Fecha Fin")
	prioridad = fields.Selection(PRIORIDADES, select=True, string="Prioridad", default=PRIORIDADES[0][0], track_visibility='onchange')
	estado = fields.Selection([('nuevo','Nuevo'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('cancel','Cancelado')], string="Estado", default='nuevo', track_visibility='onchange')

	

class ItBaseProductos(models.Model):
	_name = 'itbase.productos'
	_inherit = ['mail.thread']

	name = fields.Char(string="Nombre del Producto", track_visibility='onchange')
	dueno = fields.Many2one('res.partner', string="Dueno del Producto", track_visibility='onchange')
	responsable = fields.Many2one('itbase.departamento', string="Responsable", track_visibility='onchange')
	fecha_inicio = fields.Date(string="Fecha de Inicio", track_visibility='onchange')
	compania = fields.Many2one('itbase.equipo.compania', string="Compania", track_visibility='onchange')
	fecha_imp = fields.Date(string="Fecha de Implementacion", track_visibility='onchange')
	repositorio = fields.Char(string="Repositorio")
	proyecto = fields.Many2one('itbase.proyectos', string="Proyecto")
	otro = fields.Char(string="Otros")
	uso = fields.Char(string="Uso")
	comentarios = fields.Char(string="Comentarios")
	prioridad = fields.Selection(PRIORIDADES, select=True, string="Prioridad", default=PRIORIDADES[0][0], track_visibility='onchange')
	estado = fields.Selection([('nuevo','Nuevo'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('imple','Implementado'),
							  ('cancel','Cancelado')], string="Estado", default='nuevo', track_visibility='onchange')
	tareas_ids = fields.One2many('itbase.proyectos.tarea', 'proyecto_id', string="Tareas")
	imagen = fields.Binary(string="Logo", attachment=True)

	@api.onchange('proyecto')
	def _onchange_compania(self):
		self.compania = self.proyecto.compania



class ItBaseProyectosTareas(models.Model):
	_name = 'itbase.proyectos.tarea'
	_inherit = ['mail.thread']

	proyecto_id = fields.Many2one('itbase.productos', string="Producto" , track_visibility='onchange')
	historia_id = fields.Many2one('itbase.historias', string="Historia" , track_visibility='onchange')
	soporte_id = fields.Many2one('itbase.soporte', string="Origen", track_visibility='onchange')
	name = fields.Char(string="Tarea" , track_visibility='onchange')
	comentarios = fields.Char(string="Comentarios")
	fecha_creacion = fields.Datetime(string="Fecha de Creacion", default=fields.Datetime.now)
	fecha_inicio = fields.Date(string="Fecha de Inicio", track_visibility='onchange')
	fecha_final = fields.Date(string="Fecha Final", track_visibility='onchange')
	responsable = fields.Many2one('itbase.departamento', string="Responsable", track_visibility='onchange')
	asignada = fields.Many2one('res.users', string="Asignada", track_visibility='onchange')
	horas = fields.Char(string="En: (Horas)")
	estado = fields.Selection([('asignar','Asignada'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('espera','En espera')], string="Estado", default='espera', track_visibility='onchange')
	@api.multi
	def name_get(self):
		res = super(ItBaseProyectosTareas, self).name_get()
		result = []
		for element in res:
			proyecto_id = element[0]
			code = self.browse(proyecto_id).name
			desc = self.browse(proyecto_id).id
			name = code and '[%s] %s' % (desc, code) or '%s' % desc
			result.append((proyecto_id, name))
		return result

	@api.multi
	def asignar(self):
		for record in self:
			record.estado = 'asignar'
			record.sudo().asignada = record.env.user



class ItBaseHistorias(models.Model):
	_name = 'itbase.historias'
	_inherit = ['mail.thread']

	name = fields.Char(string="Secuencia", default="Nuevo")
	asunto = fields.Char(string="Asunto", track_visibility='onchange')
	producto_id = fields.Many2one('itbase.productos', string="Producto", track_visibility='onchange')
	responsable = fields.Many2one('itbase.departamento', string="Responsable", track_visibility='onchange')
	fecha_inicio = fields.Date(string="Fecha", track_visibility='onchange')
	fecha_final = fields.Date(string="Fecha Fin", track_visibility='onchange')
	como = fields.Char(string="Como")
	quiero = fields.Char(string="Quiero")
	para = fields.Char(string="Para")
	termino = fields.Char(string="Terminos")
	prioridad = fields.Selection(PRIORIDADES, select=True, string="Prioridad", default=PRIORIDADES[0][0], track_visibility='onchange')
	estado = fields.Selection([('nuevo','Nuevo'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('cancel','Cancelado')], string="Estado", default='nuevo', track_visibility='onchange')
	reunion_id = fields.Many2one('itbase.reuniones', string="Reunion")

	@api.multi
	def name_get(self):
		res = super(ItBaseHistorias, self).name_get()
		result = []
		for element in res:
			producto_id = element[0]
			code = self.browse(producto_id).name
			desc = self.browse(producto_id).asunto
			name = code and '[%s] %s' % (code, desc) or '%s' % desc
			result.append((producto_id, name))
		return result

	@api.model
	def create(self, vals):
		if vals.get('name', "Nuevo") == "Nuevo":
			vals['name'] = self.env['ir.sequence'].next_by_code('itbase.historias') or "Nuevo"
			return super(ItBaseHistorias, self).create(vals)

class ItBaseErrores(models.Model):
	_name = 'itbase.errores'
	_inherit = ['mail.thread']

	name = fields.Char(string="Secuencia", default="Nuevo")
	asunto = fields.Char(string="Asunto", track_visibility='onchange')
	producto_id = fields.Many2one('itbase.productos', string="Producto", track_visibility='onchange')
	tarea_id = fields.Many2one('itbase.proyectos.tarea', string="Tarea", track_visibility='onchange')
	responsable = fields.Many2one('itbase.departamento', string="Responsable", track_visibility='onchange')
	fecha_inicio = fields.Date(string="Fecha", track_visibility='onchange')
	fecha_final = fields.Date(string="Fecha Fin", track_visibility='onchange')
	descripcion = fields.Char(string="Descripcion", track_visibility='onchange')
	estado = fields.Selection([('nuevo','Nuevo'),
							  ('process','En Proceso'),
							  ('complete','Completado'),
							  ('cancel','Cancelado')], string="Estado", default='nuevo', track_visibility='onchange')
	@api.onchange('tarea_id')
	def _onchange_tarea(self):
		self.producto_id = self.tarea_id.proyecto_id

	@api.model
	def create(self, vals):
		if vals.get('name', "Nuevo") == "Nuevo":
			vals['name'] = self.env['ir.sequence'].next_by_code('itbase.errores') or "Nuevo"
			return super(ItBaseErrores, self).create(vals)