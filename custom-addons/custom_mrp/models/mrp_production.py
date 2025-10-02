from odoo import models, fields, api

class MRPProduction(models.Model):
    _inherit = 'mrp.production'

    purchase_order_id = fields.Many2one('purchase.order', string='Linked purchase order')
