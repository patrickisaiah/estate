from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'Tag names have to be uniques')]
