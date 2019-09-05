# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import datetime

class ItBaseMantenimiento(models.Model):
    _name = 'itbase.mantenimiento'
    _inherit = ['mail.thread']

    name = fields.Char(readonly=True, default="Nuevo")
    equipo_id = fields.Many2one('itbase.equipo', string="Equipo", track_visibility='onchange')
    fecha_mantenimiento = fields.Datetime(string="Fecha de Mantenimiento", track_visibility='onchange')
    tipo = fields.Selection([('cor','Corretivo'),('pre','Preventivo')], string="Tipo de Mantenimiento", track_visibility='onchange')
    fecha_programado = fields.Date(string="Fecha de Programacion", track_visibility='onchange')
#REFACCIONES - DISPOSITIVOS
    dispositivos_ids = fields.One2many('itbase.dispositivo', 'dispositivo_id', string="Dispositivos")
    estado = fields.Selection([('draft','Creado'),
                               ('espera','En Espera'),
                               ('proceso','En Proceso'),
                               ('final','Finalizado')], string="Estado", track_visibility='onchange')

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