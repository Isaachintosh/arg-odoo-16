# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class GovTaxRateLine(models.Model):
    _name = 'gov.tax.rate.line'
    _description = 'línea de tasa impositiva del gobierno'

    name = fields.Char('Nombre')
    min_value = fields.Float('Valor Mínimo')
    max_value = fields.Float('Valor Máximo')
    tax_rate = fields.Float('Tasa de Impuesto')
    gov_tax_rate_id = fields.Many2one(
        comodel_name='gov.tax.rate',
        string='Parámetro de tasa impositiva del gobierno',
    )
