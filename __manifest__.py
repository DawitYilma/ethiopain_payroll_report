# -*- coding: utf-8 -*-
{
    'name': "Payroll Report",
    'version': "10.0.1.0.0",
    'summary': """
        Report For Payroll Payslip.""",
    'description': """
        Report For Payroll Payslip.
    """,

    'author': "Dawit Yilma",
    'category': "Generic Modules/Human Resources",
    'depends': [
        "hr_payroll_community",
        "report_xlsx",
    ],
    'data': [
        'views/payroll_report.xml',
        'views/employee.xml',
        'views/company_inherit.xml',
        'reports/report.xml',
    ],
    'demo': [],
    'images': [],
    'license': "LGPL-3",
    'installable': True,
    'application': True
}
