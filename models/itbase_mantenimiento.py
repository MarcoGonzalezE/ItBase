# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from datetime import datetime

class ItBaseMantenimiento(models.Model):
    _name = 'itbase.mantenimiento'
    _inherit = ['mail.thread']

    name = fields.Char(readonly=True, default="Nuevo")
    equipo_id = fields.Many2one('itbase.equipo', string="Equipo", track_visibility='onchange')
    servidor_id = fields.Many2one('itbase.servidores', string="Servidor", track_visibility='onchange')
    tipo = fields.Selection([('corretivo','Corretivo'),('preventivo','Preventivo')], string="Tipo de Mantenimiento", track_visibility='onchange')
    base_id = fields.Many2one('itbase.basedatos', string="Base de Datos", track_visibility='onchange')
    fecha_mantenimiento = fields.Datetime(string="Fecha de Mantenimiento", track_visibility='onchange')
    fecha_programado = fields.Datetime(string="Fecha de Programacion", track_visibility='onchange')
    fecha_finalizacion = fields.Date(string="Fecha de Finalizacion", track_visibility='onchange')
    recordatorio = fields.Boolean(string="Con Recordatorio", track_visibility='onchange')
    recordatorio_id = fields.Many2one('itbase.recordatorios',string="Recordatorio")
#REFACCIONES - DISPOSITIVOS
    dispositivos_ids = fields.One2many('itbase.dispositivo', 'dispositivo_id', string="Dispositivos")
    encargado = fields.Many2one('itbase.departamento', string="Encargado")
    estado = fields.Selection([('draft','Creado'),
                               ('programado','Programado'),
                               ('proceso','En Proceso'),
                               ('final','Finalizado'),
                               ('cancel','Cancelado')], string="Estado", default='draft', track_visibility='onchange')
    descripcion = fields.Char(string="Descripcion")

    @api.model
    def create(self, vals):
        if vals.get('name', "Nuevo") == "Nuevo":
            vals['name'] = self.env['ir.sequence'].next_by_code('itbase.mantenimiento') or "Nuevo"
            return super(ItBaseMantenimiento, self).create(vals)

    @api.onchange('fecha_programado')
    def _onchange_programado(self):
        if self.fecha_programado:
            self.estado = 'programado'
        else:
            self.estado = 'draft'

    def proceso(self):
        self.estado = 'proceso'
        self.fecha_mantenimiento = datetime.now()

    def finalizado(self):
        self.estado = 'final'
        self.fecha_finalizacion = datetime.now()
        if self.equipo_id:
            if self.equipo_id.asignado:
                self.equipo_id.estado = 'assigned'
            else:
                self.equipo_id.estado = 'not_assigned'
            for e in self.dispositivos_ids:
                e.equipo_id = self.equipo_id
                e.estado = 'uso'

    def cancelado(self):
        self.estado = 'cancel'
        if self.recordatorio_id:
            self.recordatorio_id.estado = 'cancelado'
            self.recordatorio = False

    def crear_recordatorio(self):
        asunto = "Mantenimiento " + str(self.tipo) + " a "
        descripcion = str(self.name) + "\nResponsable de Mantenimiento: " + str(self.encargado.name.name) + "\nFecha de Programacion: " + self.fecha_programado
        if self.descripcion:
            descripcion += "\n" + str(self.descripcion)
        if self.equipo_id:
            asunto += str(self.equipo_id.tipo) + " [" + str(self.equipo_id.name) + "]" + str(self.equipo_id.asignado.nombre)
        if self.servidor_id:
            asunto += "servidor " + str(self.servidor_id.name)
        if self.base_id:
            asunto += "base de datos " + str(self.base_id.name)
        recordatorios = self.env['itbase.recordatorios'].create({
            'fecha' : self.fecha_programado,
            'name' : asunto,
            'responsable': self.encargado.id,
            'descripcion': descripcion
            })
        self.recordatorio_id = recordatorios.id
        self.recordatorio = True
        return {
            'name': 'Recordatorio',
            'view_id': self.env.ref('ItBase.itbase_recordatorio_form').id,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'itbase.recordatorios',
            'res_id': recordatorios.id,
            'type': 'ir.actions.act_window'
        }



class ItBaseDispositivos(models.Model):
    _name = "itbase.dispositivo"
    dispositivo_id = fields.Many2one('itbase.mantenimiento', ondelete='cascade', index=True, string="ID Dispositivo")
    equipo_id = fields.Many2one('itbase.equipo', string="Equipo", store=True, ondelete='cascade', index=True)
    name = fields.Char(string="Dispositivo/Periferico")
    estado = fields.Selection([('uso','En Uso'),
                               ('def','Reemplazado')], string="Estado")
