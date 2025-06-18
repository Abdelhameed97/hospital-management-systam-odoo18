from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    #  Basic Fields
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    #  Department Relation
    department_id = fields.Many2one('hms.department', string='Department')

    # ️ Doctors Relation
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')

    # 🩺 Health Status
    state = fields.Selection(
        [
            ('undetermined', 'Undetermined'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('serious', 'Serious'),
        ],
        string='Health Status',
        default='undetermined'
    )

    #  Log History
    log_history_ids = fields.One2many('hms.log_history', 'patient_id', string='Log History')

    # 💉 PCR and CR
    pcr = fields.Boolean(string='PCR')
    cr_ratio = fields.Float(string='CR Ratio')

    # History + Computed Age
    history = fields.Text(string='History')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    #  Age Calculation
    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year

    #  Log creation when state changes (inside form)
    @api.onchange('state')
    def _onchange_state(self):
        if self.state and self.id:
            self.log_history_ids |= self.env['hms.log_history'].create({
                'description': f"State changed to {self.state}",
                'patient_id': self.id,
                'created_by': self.env.uid,
            })

    # Automatic PCR check if age < 30
    @api.onchange('age')
    def _onchange_age_pcr(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Automatically Checked",
                    'message': "PCR was automatically checked because age is under 30."
                }
            }

    # Prevent assigning patient to closed department
    @api.constrains('department_id')
    def _check_department_open(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("You cannot assign a patient to a closed department.")

    #  If PCR is checked, CR Ratio must be filled
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

