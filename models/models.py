from odoo import models, fields, api
import base64
from odoo.modules.module import get_module_resource

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    total_hours = fields.Integer(string='Total Hours', states={'done': [('readonly', True)]},
                                help='Total Hours Of Working schedule', compute="compute_total_hours")

    def compute_total_hours(self):
        for line in self.worked_days_line_ids:
            self.total_hours += line.number_of_hours if line.code == 'WORK100' else 0.0
        return {
            'total_hours': self.total_hours,
        }


class Company(models.Model):
    _inherit = 'res.company'

    owner = fields.Many2one("res.users", string="Owner")
