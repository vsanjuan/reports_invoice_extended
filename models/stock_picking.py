# -*- coding: utf-8 -*-
from openerp import models, api, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    note = fields.Text(
        help="Introduzca aquí las observaciones que se mostrarán en el albarán")


    @api.one
    def get_delivery_address(self, partner_id):
        res = {}
        partner_obj = self.env['res.partner']
        partner = partner_obj.browse(partner_id)
        if partner:
            res = {
                'name': partner.name,
                'street': partner.street,
                'city': partner.city,
                'zip': partner.zip,
                'country': partner.country_id.name,
                'notes': partner.comment,
                'contact_ref': partner.ref,
                'phone': partner.phone or partner.mobile
            }
        return res

    @api.one
    def get_client_ref(self):
        so_obj = self.env['sale.order']
        if self.origin:
            origin = so_obj.search([
                ('name', '=', self.origin)
            ])
            return origin.client_order_ref
        return False

    @api.one
    def get_labels(self):
        res = []
        for move in self.move_lines:
            res.append(move.product_id.default_code)
        return res

    @api.one
    def get_labels_number(self):
        total = 0
        for move in self.move_lines:
            total += move.number_of_packages
        return total
