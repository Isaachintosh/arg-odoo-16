# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class GovTaxGuide(models.Model):
    _name = 'gov.tax.guide'
    _description = 'Guía de pago de impuestos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nombre'
    )
    
    property_id = fields.Many2one(
        comodel_name='res.partner.property',
        string="Imóvel",
        required=True
    )
    
    owner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Proprietário",
        related="property_id.owner_id",
        store=True
    )
    
    tax_rate_id = fields.Many2one(
        comodel_name='gov.tax.rate',
        string="Taxa de Imposto",
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Moeda',
        default=lambda self: self.env.company.currency_id
    )
    
    tax_amount = fields.Monetary(
        string="Valor do Imposto",
        compute="compute_tax_amount",
        currency_field="currency_id",
        store=True
    )
    
    invoice_date = fields.Date(string="Data de Emissão")
    payment_date = fields.Date(string="Data de Vencimento")
    
    status = fields.Selection([
        ('draft', 'Borrador'),
        ('generated', 'Gerado'),
        ('paid', 'Pago'),
        ('cancelled', 'Cancelado')
    ], string="Situación", default='draft')
