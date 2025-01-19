# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class GovTaxRateLine(models.Model):
    _name = 'gov.tax.rate.line'
    _description = 'línea de tasa impositiva del gobierno'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nombre'
    )
    
    min_value = fields.Float(
        string='Valor Mínimo',
        digits=(16, 2)
    )
    
    max_value = fields.Float(
        string='Valor Máximo',
        digits=(16, 2)
    )
    
    tax_rate = fields.Float(
        string='Tasa de Impuesto',
        digits=(16, 4)
    )
    
    gov_tax_rate_id = fields.Many2one(
        comodel_name='gov.tax.rate',
        string='Parámetro de tasa impositiva del gobierno',
    )
