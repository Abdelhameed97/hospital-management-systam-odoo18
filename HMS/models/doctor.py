from odoo import models,fields

class HMSDoctor (models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Binary(string='Photo')


