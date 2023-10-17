from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Description"
    _order = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record['offer_count'] = len(record.offer_ids)


class EstatePropertyLine(models.Model):
    _name = "estate.property.line"
    _description = "Estate Property Line"






