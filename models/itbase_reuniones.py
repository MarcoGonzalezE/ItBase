# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

class ItBaseReuniones(models.Model):
	_name = 'itbase.reuniones'
	_inherit = ['mail.thread']

	name = fields.Char(string="Tema")
	fecha = fields.Date(string="Fecha")
	asistencia = fields.Many2many('res.partner', string="Asistentes")
	area = fields.Many2one('itbase.soluciones.area', string="Area", track_visibility='onchange')
	producto = fields.Many2one('itbase.productos', string="Producto", track_visibility='onchange')
	compania = fields.Many2one('itbase.equipo.compania', string="Compania")
	historia_ids = fields.One2many('itbase.historias', 'reunion_id', string="Historias")