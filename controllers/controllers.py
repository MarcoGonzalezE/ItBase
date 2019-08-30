# -*- coding: utf-8 -*-
from odoo import http

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