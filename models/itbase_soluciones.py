# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools

class ItBase_Soluciones(models.Model):
	_name = 'itbase.soluciones'
	_inherit = ['mail.thread']

	name = fields.Char(string="Problema", track_visibility='onchange')
	area = fields.Many2one('itbase.soluciones.area', string="Area", track_visibility='onchange')
	resumen = fields.Char(string="Solucion")
	url = fields.Char(string="Referencia")

class ItBase_Soluciones_Area(models.Model):
	_name = 'itbase.soluciones.area'

	name = fields.Char(string="Area")

class ItBaseSolucionesDashboard(models.Model):
	_name = 'itbase.soluciones.dashboard'

	name = fields.Char(string="Area")
	color = fields.Integer(string="Color")
