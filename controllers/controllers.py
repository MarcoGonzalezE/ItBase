# -*- coding: utf-8 -*-
from odoo import http
#import request

# class Itbase(http.Controller):
#     @http.route('/itbase/itbase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/itbase/itbase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('itbase.listing', {
#             'root': '/itbase/itbase',
#             'objects': http.request.env['itbase.itbase'].search([]),
#         })

#     @http.route('/itbase/itbase/objects/<model("itbase.itbase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('itbase.object', {
#             'object': obj
#         })

# class ItBaseController(http.Controller):
# 	@http.route('/soluciones/ticket/enviar', type="http", auth="public", website=True)
# 	def itbase_enviar_ticket(self,""kw):
# 		person_name = ""
# 		person_name = http.request.env.user.name
# 		return http.request.render('Itbase.itbase_enviar_ticket',
# 			{
# 			'solicitante': person_name,
# 			'correo' : http.request.env.user.email
# 			})
	