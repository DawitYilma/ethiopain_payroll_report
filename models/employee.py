from odoo import models, fields, api

class Employee(models.Model):
    _inherit = 'hr.employee'

    tin_number = fields.Char('Tin Number')