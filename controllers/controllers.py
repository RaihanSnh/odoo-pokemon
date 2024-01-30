# -*- coding: utf-8 -*-
# from odoo import http


# class OdooPokemon(http.Controller):
#     @http.route('/odoo_pokemon/odoo_pokemon', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_pokemon/odoo_pokemon/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_pokemon.listing', {
#             'root': '/odoo_pokemon/odoo_pokemon',
#             'objects': http.request.env['odoo_pokemon.odoo_pokemon'].search([]),
#         })

#     @http.route('/odoo_pokemon/odoo_pokemon/objects/<model("odoo_pokemon.odoo_pokemon"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_pokemon.object', {
#             'object': obj
#         })

