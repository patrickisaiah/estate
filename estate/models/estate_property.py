from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import api, fields, models, _
from odoo import exceptions
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    property_reference = fields.Char(string='Property Reference',
                                     required=True, copy=False,
                                     readonly=True,
                                     index=True,
                                     default=lambda self: _('New'))

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Availability Date", copy=False,
                                    default=datetime.today() + relativedelta(months=1))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False, compute="_compute_selling_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')], default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", copy=False, string="Buyer")
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Seller")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    property_image = fields.Binary('Image')

    _sql_constraints = [
        ('check_positive_ep', 'CHECK(expected_price >= 0 )',
         'The expected price should be more than 0.'),

        ('check_positive_sp', 'CHECK(selling_price >= 0)', 'The selling price must be positive'),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record["total_area"] = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        if self.offer_ids:
            self.best_price = max(self.offer_ids.mapped('price'))
        else:
            self.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "east"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("Cancelled Property cannot be sold")
            else:
                record["state"] = "sold"
        return True

    def action_property_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Sold Property cannot be cancelled")
            else:
                record["state"] = "canceled"
        return True

    @api.depends('offer_ids.status')
    def _compute_selling_price(self):
        for record in self:
            if record.offer_ids:
                record['state'] = 'offer_received'
                for line in record.offer_ids:
                    if line.status == "accepted":
                        record['selling_price'] = line.price
                        record['buyer_id'] = line.partner_id
                        record['state'] = 'offer_accepted'
                        break
                    else:
                        record['selling_price'] = 0.00
            else:
                record['selling_price'] = 1.00

    # @api.constrains('selling_price', 'expected_price')
    # def _check_selling_price(self):
    #     for record in self:
    #         if record.selling_price < record.expected_price * 0.9 and record.selling_price != 0:
    #             raise ValidationError('Error Message.')

    def unlink(self):
        for prop in self:
            if prop.state not in ('new', 'canceled'):
                raise UserError('You cannot delete a property which is not new or cancelled.')
        return models.Model.unlink(self)

    @api.onchange('offer_ids')
    def is_offer_lower(self):
        for record in self:
            if record.offer_ids:
                if record.offer_ids[-1].price < record.offer_ids[-2].price:
                    raise UserError("The offer you are entering is lower than existing offers")

    @api.model
    def create(self, vals):
        if vals.get('property_reference', _('New') == _('New')):
            vals['property_reference'] = self.env['ir.sequence'].next_by_code('estate.property') or _('New')
            res = super(EstateProperty, self).create(vals)
        return res
















