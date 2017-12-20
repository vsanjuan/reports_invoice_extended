# -*- coding: utf-8 -*-
from openerp import models, api, fields, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF, DEFAULT_SERVER_DATETIME_FORMAT as DFT
from datetime import datetime


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
    def get_origin(self, origin, condition):
        so_obj = self.env['sale.order']
        picking_obj = self.env['stock.picking']
        sale = False
        if origin:
            # Search origin in Sales order
            sale = so_obj.search([
                ('name', '=', origin)
            ])
            if not sale:
                # Search origin in Stock Picking
                picking = picking_obj.search([
                    ('name', '=', origin)
                ])
                if picking:
                    # Search origin in Sales order
                    sale = so_obj.search([
                        ('name', '=', picking.origin)
                    ])
        if sale:
            if condition == 'origin':
                return sale.name
            elif condition == 'client_ref':
                return sale.client_order_ref
            elif condition == 'so_date':
                date = datetime.strptime(sale.date_order, DFT)
                return date.strftime("%d/%m/%Y")
        return False

    @api.one
    def get_discount(self):
        discount = 0
        for line in self.invoice_line:
            if line.discount > 0:
                discount += line.price_unit * (line.discount / 100)
        return discount
