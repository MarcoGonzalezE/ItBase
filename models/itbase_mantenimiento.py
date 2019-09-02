# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

class ItBaseMantenimiento(models.Model):
    _name = 'itbase.mantenimiento'

    name = fields.Char(readonly=True, default="Nuevo")
    equipo_id = fields.Many2one('itbase.equipo', string="Equipo")
    fecha_mantenimiento = fields.Datetime(string="Fecha de Mantenimiento")
    tipo = fields.Selection([('cor','Corretivo'),('pre','Preventivo')], string="Tipo de Mantenimiento")
    fecha_programado = fields.Date(string="Fecha de Programacion")
#REFACCIONES - DISPOSITIVOS
    dispositivos_ids = fields.One2many('itbase.dispositivo', 'dispositivo_id', string="Dispositivos")
    estado = fields.Selection([('draft','Creado'),
                               ('espera','En Espera'),
                               ('proceso','En Proceso'),
                               ('final','Finalizado')], string="Estado")

    @api.model
    def create(self, vals):
        if vals.get('name', "Nuevo") == "Nuevo":
            vals['name'] = self.env['ir.sequence'].next_by_code('itbase.mantenimiento') or "Nuevo"
            return super(ItBaseMantenimiento, self).create(vals)

class ItBaseDispositivos(models.Model):
    _name = "itbase.dispositivo"
    dispositivo_id = fields.Many2one('itbase.mantenimiento', string="ID Dispositivo")
    name = fields.Char(string="Dispositivo/Periferico")
    estado = fields.Selection([('uso','En Uso'),
                               ('def','Reemplazado')], string="Estado")