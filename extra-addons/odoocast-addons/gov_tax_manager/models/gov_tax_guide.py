# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class GovTaxGuide(models.Model):
    _name = 'gov.tax.guide'
    _description = 'Guía de pago de impuestos'

    name = fields.Char('Nombre')
    # property_id = fields.Many2one('res.pertner.property', string="Imóvel", required=True)
    # owner_id = fields.Many2one('res.partner', string="Proprietário", related="property_id.owner_id", store=True)
    # tax_amount = fields.Float(string="Valor do Imposto", related="property_id.tax_rate_id", store=True)
    payment_date = fields.Date(string="Data de Vencimento", required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('paid', 'Pago'),
        ('cancelled', 'Cancelado')
    ], string="Situación", default='draft', required=True)
