# -*- coding: utf-8 -*-
{
    'name': "Reports Invoice Extended",

    'summary': """Reports Invoice Extended""",

    'description': "", # Dejar vacio para que coja el README.rst

    'author': "Acelerem",
    'website': "http://odoo.acelerem.com",
    # Category se usa com filtro para la lista de modulos
    'category': 'Account',
    'version': '8.0.0.1.5',
    'license': 'AGPL-3',
    # Depends indica los modulos necesarios para el correcto trabajo de nuestro modulo
    'depends': [
        'account',
        'stock',
        'sale',
        #'account_payment_partner' #Repositorio bank-payment de OCA
    ],  # es una lista porque puede depender de mas de uno
    # Datos que siempre carga
    'data': [
        'views/invoice_group_picking_report.xml',
    ],
    "installable": True,
}
