# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class GovTaxRate(models.Model):
    _name = 'gov.tax.rate'
    _description = 'Tasa de impuesto del gobierno'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nombre'
    )
    
    antecipated_payment_tax_discount = fields.Float(
        string="Descuento fiscal por pago anticipado",
        digits=(16, 2),
        default=0
    )
    
    inarrengement_payment_tax_discount = fields.Float(
        string="Descuento de impuestos por pago irregular",
        digits=(16, 2),
        default=0
    )
    
    tax_line_ids = fields.One2many(
        comodel_name='gov.tax.rate.line',
        inverse_name='gov_tax_rate_id',
        string='Líneas de impuestos',
    )
    
    account_move_ids = fields.One2many(
        comodel_name='account.move',
        inverse_name='gov_tax_rate_id',
        string='Facturas',
    )
    
    building_type = fields.Selection(
        selection=[
            ('residential', 'Residencial'),
            ('commercial', 'Comercial'),
            ('industrial', 'Industrial'),
            ('rural', 'Rural'),
        ],
        string='Tipo de edificio',
        default='residential'
    )
    
    location_type = fields.Selection(
        selection=[
            ('urban', 'Urbano'),
            ('rural', 'Rural'),
        ],
        string='Tipo de ubicación',
        default='urban'
    )
    
    status = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('approved', 'Aprobado'),
            ('active', 'Activo'),
            ('inactive', 'Inactivo'),
            ('canceled', 'Cancelado'),
        ],
        string='Situación',
        default='draft'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )
    
    def action_approve(self):
        self.status = 'approved'
    
    def action_activate(self):
        self.status = 'active'
    
    def action_cancel(self):
        self.status = 'canceled'
    
    def action_inactive(self):
        self.status = 'inactive'
    
    def action_draft(self):
        self.status = 'draft'