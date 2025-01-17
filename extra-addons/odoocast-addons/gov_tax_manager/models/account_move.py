# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    gov_tax_rate_id = fields.Many2one(
        comodel_name='gov.tax.rate',
        string='Tasa de impuesto del gobierno',
    )