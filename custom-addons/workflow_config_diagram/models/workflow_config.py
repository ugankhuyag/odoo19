from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class WorkflowConfig(models.Model):
    _name = 'workflow.config'

    is_active = fields.Boolean(string='Active', default=True)
    name = fields.Char('Name', required=True)
    template_id = fields.Many2one('mail.template', string='Email template')
    line_ids = fields.One2Many('workflow.config.line', 'config_id','Config Line')
    department_id = fields.Many2one('hr.department', string='Department')
    company_id = fields.Many2one('res.company', string='Company')
    model_id = fields.Many2one('ir.model', string='Model')

class WorkflowConfigLine(models.Model):
    STATE_SELECTION = [
        ('waiting', 'Waiting'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('return', 'Return'),
        ('rejected', 'Rejected'),
    ]

    name = fields.Char(string='Name', size=128, required=True)
    config_id = fields.Many2one('workflow.config', string='Workflow Config', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', required=True, default=1)
    type = fields.Selection([
        ('creator', 'Creator'),
        ('fixed', 'Fixed'),
        ('department', 'Department'),
        ('group','Group')], string='Type', required=True, default='fixed')
    user_id = fields.Many2one('res.users', string='User')
    group_id = fields.Many2one('res.groups', string='Group')
    expression = fields.Text(string='Expression', default='True')
    return_sequence = fields.Integer(string='Return Sequence')
    is_inside_department = fields.Boolean('Is inside department')

    _sql_constraints = [
        ('sequence_nonzero', 'check(sequence > 0)', 'Sequence must be greater than zero!')
    ]

    @api.onchange('type')
    def onchange_type(self):
        self.update({
            'user_id': False,
            'group_id': False
        })

    def write (self, vals):
        if vals.get('type') == 'creator':
            vals.update({
                'user_id': False,
                'group_id': False,
            })
        if vals.get('type') == 'fixed':
            vals.update({
                'user_id': False
            })
        if vals.get('type') == 'group':
            vals.update({
                'user_id': False
            })
        if vals.get('type') == 'depart':
            vals.update({
                'user_id': False,
                'group_id': False,
            })
        return super(WorkflowConfigLine, self).write(vals)
