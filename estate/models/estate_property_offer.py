from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')],
                              readonly=True, copy=False, default='pending')
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)


    _sql_constraints = [('positive_price', 'CHECK(price >=0)', 'Offer price must be positive number')]

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            num_of_days = record.validity
            record['date_deadline'] = datetime.today() + relativedelta(days=num_of_days)

    def _inverse_deadline(self):
        for record in self:
            record['validity'] = (record.date_deadline - datetime.now().date()).days

    def action_accept(self):
        for record in self:
            record['status'] = 'accepted'

    def action_reject(self):
        for record in self:
            record['status'] = 'rejected'


