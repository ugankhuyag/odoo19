
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class MRPProduction(models.Model):
    _inherit = 'mrp.production'

    purchase_order_id = fields.Many2one('purchase.order', string='Linked purchase order')

    def action_check_product_cost(self):

        if not self:
            self = self.env['mrp.production'].search([])

        ids = []

        for obj in self:
            try:
                stock_moves = self.env['stock.move'].search(['|',
                                                             ('production_id','=', obj.id),
                                                             ('raw_material_production_id','=', obj.id)])
                print("\n", stock_moves)
                for move in stock_moves:
                    if move.account_move_id:
                        print("move is connected", move.product_id.name, move.production_id)
                    else:
                        print("move is not connected", move.product_id.name, move.raw_material_production_id)

                    journal_id = move.product_id.categ_id.property_stock_journal_id

                    if not journal_id:
                        raise ValueError("Journal not found.")
                    currency_id = self.env.company.currency_id
                    cost = move.product_id.standard_price * move.product_qty

                    move_line_vals = {
                        'name': move.product_id.name,
                        'product_id': move.product_id.id,
                        'currency_id': currency_id.id,
                        'display_id': 'product'
                    }

                    if move.raw_material_production_id:
                        debit_account_id = move.product_id.category_id.mrp_income_account_id
                        credit_account_id = move.product_id.category_id.mrp_expense_account_id
                    else:
                        debit_account_id = move.product_id.category_id.mrp_income_account_id
                        credit_account_id = move.product_id.category_id.mrp_expense_account_id


                    debit_move_line_vals = move_line_vals.copy()
                    debit_move_line_vals.update({
                        'debit': cost,
                        'account_id': debit_account_id.id,
                    })
                    credit_move_line_vals = move_line_vals.copy()
                    credit_move_line_vals.update({
                        'credit': cost,
                        'account_id': credit_account_id.id,
                    })

                    if not journal_id.currency_id:
                        raise ValidationError("Currency not found." + journal_id.name)

                    account_move_id = self.env['account.move'].create({
                        'journal_id': journal_id.id,
                        'move_type': 'entry',
                        'invoice_date': fields.Date.today(),
                        'currency_id': journal_id.currency_id.name,
                        'invoice_line_ids': [(0, 0, debit_move_line_vals),
                                             (0, 0, credit_move_line_vals)]
                        })
                    ids.append(account_move_id.id)

                    print("\n\n", account_move_id.id, account_move_id.name)
            except Exception as e:
                print ("\n\neeee", e)
                continue

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "views": [[False, "list"],[False, "kanban"], [False, "form"]],
            "context": {"create": False},
            "domain": [["id", "in", ids]],
        }