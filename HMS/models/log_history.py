from odoo import models, fields

class HMSLogHistory(models.Model):
    _name = 'hms.log_history'
    _description = 'Log History for Patient State'

    description = fields.Text(string='Description')
    date = fields.Datetime(string='Date', default=lambda self: fields.Datetime.now())
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.uid
    )
    patient_id = fields.Many2one(
        'hms.patient',
        string='Patient'
    )
