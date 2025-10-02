from odoo import models, fields, api
from odoo.exceptions import UserError

print("=" * 50)
print("🔥 LOADING custom_mrp/models/purchase_order.py")
print("=" * 50)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    for_production = fields.Boolean(string='For productions', default=False)
    production_doc_number = fields.Char(string='Production Doc Number')
    mrp_production_id = fields.Many2one('mrp.production', string='MRP Production', readonly=True)

    def init(self):
        print("✅ PurchaseOrderLine loaded with production_doc_number field")
        super().init()


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def create_mrp_from_purchase(self):
        mrp_obj = self.env['mrp.production']
        mrp_bom_obj = self.env['mrp.bom']
        mrp_bom_line_obj = self.env['mrp.bom.line']

        for line in self.order_line:
            # Check if MRP already exists for this PO
            mrp_purchase_ids = mrp_obj.search([('purchase_order_id', '=', self.id)])
            print(mrp_purchase_ids, '<<<<mrp_purchase_id')

            # Find BOM line with this product
            mrp_bom_line_id = mrp_bom_line_obj.search([('product_tmpl_id', '=', line.product_id.id)])
            print(mrp_bom_line_id)

            # Get BOM ID from the line, or False if not found
            mrp_bom_id = mrp_bom_line_id.bom_id if mrp_bom_line_id.bom_id else False
            print(mrp_bom_line_id.read())

            if mrp_purchase_ids:
                raise UserError('Холбоотой үйлдвэрлэл аль хэдийн үүссэн байна.')
            else:
                product_id = self.env['product.product'].search(
                    [('product_tmpl_id', '=', mrp_bom_id.product_tmpl_id.id)])
                mrp_order_id = mrp_obj.create({
                    'product_id': product_id.id,
                    'product_qty': line.product_qty * mrp_bom_id.product_qty,
                    'purchase_order_id': self.id,
                    'bom_id': mrp_bom_id.id if mrp_bom_id else False,  # ✅ Fixed this line
                })
                line.mrp_production_id = mrp_order_id.id

                print(mrp_order_id, mrp_order_id.purchase_order_id, '<<<<<<<<<<<<<MRP ORDER')

        # Return to view created MRPs
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manufacturing Orders',
            'res_model': 'mrp.production',
            'view_mode': 'list,form',
            'domain': [('purchase_order_id', '=', self.id)],
            'target': 'current',
        }
