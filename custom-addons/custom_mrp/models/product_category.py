from email.policy import default

from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_stock_journal_id = fields.Many2one('account.journal', string='Journal')
    is_mrp_accounting = fields.Boolean(string='MRP category', default=False)
    mrp_income_account_id = fields.Many2one('account.account', string='Income Account')
    mrp_expense_account_id = fields.Many2one('account.account', string='Expense Account')
