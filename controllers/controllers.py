# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class ItBaseController(http.Controller):
	@http.route('/soporte/ticket', type="http", auth="public", website=True)
	def itbase_soporte_ticket(self,**kwargs):
		person_name = ""
		correo = ""
		if http.request.env.user.name != "Public user":
			person_name = http.request.env.user.name
			correo = http.request.env.user.email
		return http.request.render('ItBase.itbase_enviar_ticket',
			{
			'solicitante_id': person_name,
			'correo' : correo,
			'companias': http.request.env['itbase.equipo.compania'].sudo().search([]),
			'equipos': http.request.env['itbase.equipo'].sudo().search([]),
			})

	@http.route('/soporte/ticket/equipos', type='http', auth="public", website=True)
	def soporte_ticket_equipos(self, **kwargs):
		values = {}
		for field_name, field_value in kwargs.items():
			values[field_name] = field_value

		person_name = ""
		result = ""
		if http.request.env.user.name != "Public user":
			person_name = http.request.env.user.name
			asignado = request.env['itbase.equipo.asignar'].sudo().search([('nombre','=', person_name)])
			equipos = request.env['itbase.equipo'].sudo().search([('company_id','=', int(values['compania'])),('asignado','in', asignado.ids)], order='name asc',)
			if equipos:
				equipos = request.env['itbase.equipo'].sudo().search([('company_id', '=', int(values['compania'])), ('asignado', 'in', asignado.ids)],order='name asc', )
			else:
				equipos = request.env['itbase.equipo'].sudo().search([('company_id','=', int(values['compania']))], order='name asc',)
		else:
			equipos = request.env['itbase.equipo'].sudo().search([('company_id','=', int(values['compania']))], order='name asc',)

		if equipos:
			result += "<div class=\"form-group\">\n"
			result += "    <label class=\"col-md-3 col-sm-4 control-label\" for=\"equipment\">EQUIPO</label>\n"
			result += "    <div class=\"col-md-7 col-sm-8\">\n"
			result += "			<select class=\"form-control\" id=\"equipo\" name=\"equipo\">\n"
			result += "            <option value="">" + "SELECCIONE EQUIPO..." + "</option>\n"
			for equipo_id in equipos:
				result += "            <option value=\"" + str(equipo_id.id) + "\">" + "["+ equipo_id.name.encode("utf-8") + "] " + str(equipo_id.marca.name) + " - " + str(equipo_id.asignado.nombre) + "</option>\n"
			result += "        </select>\n"
			result += "    </div>\n"
			result += "</div>\n"
		return result

	@http.route('/soporte/ticket/enviar', type="http", auth="public", website=True, csrf=True)
	def itbase_soporte_ticket_enviar(self, **kwargs):
		values = {}
		for field_name, field_value in kwargs.items():
			values[field_name] = field_value
		nuevo = request.env['itbase.soporte'].sudo().create({'solicitante_id':values['solicitante_id'], 'correo':values['correo'], 'compania':values['compania'], 'equipo_id':values['equipo'], 'name':values['name'], 'descripcion':values['descripcion']})
		return http.request.render('ItBase.itbase_soporte_ticket_enviado', 
			{
			'soporte': nuevo.seq
			})