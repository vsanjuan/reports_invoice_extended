# -*- coding: utf-8 -*-
from openerp import models, api, fields, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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
    def get_discount(self):
        discount = 0
        for line in self.invoice_line:
            if line.discount > 0:
                discount += line.price_unit * (line.discount / 100)
        return discount
