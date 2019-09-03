# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools

class ItBase_Soluciones(models.Model):
	_name = 'itbase.soluciones'

	name = fields.Char(string="Problema")
	area = fields.Many2one('itbase.soluciones.area', string="Area")
	resumen = fields.Char(string="Solucion")
	url = fields.Char(string="Referencia")

class ItBase_Soluciones_Area(models.Model):
	_name = 'itbase.soluciones.area'

	name = fields.Char(string="Area")

class ItBaseSolucionesDashboard(models.Model):
	_name = 'itbase.soluciones.dashboard'

	name = fields.Char(string="Area")
	color = fields.Integer(string="Color")
