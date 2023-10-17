from odoo import http
from odoo.http import Controller, request, route

class Estate(http.Controller):
    @http.route(['/estate/estates'], auth="public", website=True)
    def estate_listing(self, **post):
        return http.request.render("estate.estate_listing", {
            'properties': http.request.env['estate.property'].search([]),
        })

    @http.route('/hello4/', type='http', auth="public", website=True)
    def plants_hello4(self, **post):
        values = {
            'company': http.request.env.user.company_id.sudo(),
            'properties': http.request.env['estate.property'].search([]),
        }
        return http.request.render("estate.frontend_layout", values)

    @http.route('/estate/create/', type='http', auth="public", website=True)
    def webform(self, **post):
        return http.request.render("estate.create_estate", {})
    
    @http.route('/create/estate_property/', type='http', auth="public", website=True)
    def create_estate(self, **post):
        print("Data received........", post)
        request.env['estate.property'].sudo().create(post)
        return http.request.render("estate.estate_create_thanks", {})



    # @http.route('/estate/estate/objects/', auth='public', website=True)
    # def list(self, **kw):
    #     return http.request.render('estate.listing', {
    #         'root': '/estate/estate',
    #         'objects': http.request.env['estate.property'].search([]),
    #     })
    #
    # @http.route('/estate/estate/objects/<model("estate.property"):obj>/', auth='public', website=True)
    # def object(self, obj, **kw):
    #     return http.request.render('estate.object', {
    #         'object': obj
    #     })

