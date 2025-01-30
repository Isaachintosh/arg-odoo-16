# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartnerProperty(models.Model):
    _name = 'res.partner.property'
    _description = 'Registro de Imóvel'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre')
    
    owner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Proprietário"
    )
    
    fiscal_building_value = fields.Monetary(
        string="Valor Fiscal do Imóvel",
        currency_field='currency_id'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Moeda',
        default=lambda self: self.env.company.currency_id
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
    
    # dirección
    street = fields.Char(
        string='Camino'
    )
    
    number = fields.Char(
        string='Número'
    )
    
    neighborhood = fields.Char(
        string='Vecindario'
    )
    
    city = fields.Char(
        string='Ciudad'
    )
    
    state = fields.Char(
        string='Estado'
    )
    
    country = fields.Many2one(
        comodel_name='res.country',
        string='País'
    )
    
    zip = fields.Char(
        string='Código Postal'
    )
