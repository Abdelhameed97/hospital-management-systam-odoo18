{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Hospital Management System',
    'description': """
        Hospital Management System module for managing:
        * Patients
        * Patient Records
        * Medical History
    """,
    'sequence': -100,
    'author': 'HMS',
    'website': 'www.hms.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'views/log_history_view.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}