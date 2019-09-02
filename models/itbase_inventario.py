# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools

# class itbase(models.Model):
#     _name = 'itbase.itbase'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class ItBase_Equipo(models.Model):
	_name = 'itbase.equipo'

	name = fields.Char(readonly=True, default="Nuevo")
	marca = fields.Many2one('itbase.marca', string="Marca", track_visibility='onchange')
	modelo = fields.Char(string="Modelo", track_visibility='onchange')
	so_id = fields.Many2one('itbase.so', string="Sistema Operativo", track_visibility='onchange')
	procesador = fields.Char()
	ram = fields.Integer()
	tipo = fields.Selection([('escritorio','Escritorio'),
							('laptop','Laptop')],
							string="Tipo", track_visibility='onchange')
	arquitectura = fields.Selection([('x_32','32 bits'),('x_64','64 bits')], string="Arquitectura")
	estado = fields.Selection([('created','Creado'),
								('not_assigned','Sin Asignnar'),
								('assigned','Asignado'),
								('repair','Reparacion'),
								('maintenance','Mantenimiento'),
								('scrap','Desecho')],
								string = "Estado", track_visibility='onchange')
	imagen_variante = fields.Binary(attachment=True)
	imagen = fields.Binary(string="Imagen Computadora", attachment=True)
	imagen_small = fields.Binary(attachment=True)
	imagen_medium = fields.Binary(attachment=True)
	company_id = fields.Many2one('res.company', string="Compañia", default=lambda self: self.env['res.company']._company_default_get('itbase.equipo'))

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
			
	@api.model
	def create(self, vals):
		if vals.get('name', "Nuevo") == "Nuevo":
			vals['name'] = self.env['ir.sequence'].next_by_code('itbase.equipo') or "Nuevo"
			return super(ItBase_Equipo, self).create(vals)

#CONTADOR DE MANTENIMIENTOS
	mantenimiento = fields.One2many('itbase.mantenimiento', 'equipo_id', string="Mantenimientos")
	mantenimiento_count = fields.Integer(compute="_count_mantenimiento", string="Mantenimientos")
	mantenimientos = fields.Char(compute="_count_mantenimientos", string="Mantenimientos")

	@api.one
	@api.depends('mantenimiento')
	def _count_mantenimiento(self):
		self.mantenimiento_count = self.mantenimiento.search_count([('equipo_id','=',self.id)])

	@api.one
	@api.depends('mantenimiento_count')
	def _count_mantenimientos(self):
		self.mantenimientos = str(self.mantenimiento_count)

#DISPOSITIVOS EXTRA
	dispositivos_ids = fields.One2many('itbase.dispositivo', 'dispositivo_id', string='Dispositivos')

#PROGRAMAS ADICIONALES - LICENCIAS
	licencia_ids = fields.One2many('itbase.licencia', 'equipo_id', string="Licencias")

#HISTORIAL DE ASIGNACIONES
	asignar_ids = fields.One2many('itbase.equipo.asignar', 'equipo_id', string="Asignaciones")


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

class AsigacionEquipo(models.Model):
	_name =	'itbase.equipo.asignar'
	equipo_id = fields.Many2one('itbase.equipo', string='Equipo')
	name = fields.Many2one('res.partner', string="Asignada(o)")
	correo = fields.Char(string="Correo")
	departamento = fields.Char(string="Departamento")
	fecha_asignacion = fields.Date(string="Fecha de Asignacion")
	fecha_devolucion = fields.Date(string="Fecha de Devolucion")
	nota = fields.Char(string="Nota")

	@api.multi
	@api.onchange('name')
	def _correo_asignado(self):
		self.correo = self.name.email

