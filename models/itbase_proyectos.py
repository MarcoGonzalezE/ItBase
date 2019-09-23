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

	name = fields.Char(string="Nombre del Producto")
	dueno = fields.Many2one('res.partner', string="Dueno del Producto")
	responsable = fields.Many2one('itbase.departamento', string="Responsable")
	fecha_inicio = fields.Date(string="Fecha de Inicio")
	compania = fields.Many2one('itbase.equipo.compania', string="Compania")
	fecha_imp = fields.Date(string="Fecha de Implementacion")
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

	@api.onchange('proyecto')
	def _onchange_compania(self):
		self.compania = self.proyecto.compania



class ItBaseProyectosTareas(models.Model):
	_name = 'itbase.proyectos.tarea'

	proyecto_id = fields.Many2one('itbase.productos', string="Producto")
	name = fields.Char(string="Tarea")
	comentarios = fields.Char(string="Comentarios")
	fecha_inicio = fields.Date(string="Fecha de Inicio")
	fecha_final = fields.Date(string="Fecha Final")
	responsable = fields.Many2one('itbase.departamento', string="Asignada")
	estado = fields.Selection([('process','En Proceso'),
							  ('complete','Completado'),
							  ('espera','En espera')], string="Estado", default='espera', track_visibility='onchange')
