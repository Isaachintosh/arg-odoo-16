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
    
    city_department = fields.Integer(
        string="Departamento/Município"
    )
    
    zone_or_session_cad = fields.Integer(
        string="Zona ou Seção Cadastral"
    )
    
    quarter_number = fields.Integer(
        string="Manzana (Quadra)"
    )
    
    installment_lot_number = fields.Integer(
        string="Parcela/Lote"
    )
    
    sub_installment_number = fields.Integer(
        string="Subparcelas (se aplicável)"
    )
    
    auto_generate_build_code = fields.Boolean(
        string="Gerar código de edificio automaticamente",
        default=True
    )

    @api.depends('city_department','zone_or_session_cad','quarter_number','installment_lot_number','sub_installment_number')
    @api.onchange('city_department','zone_or_session_cad','quarter_number','installment_lot_number','sub_installment_number')
    def compute_name(self):
        for record in self:
            name = ""
            separator = "-"
            if record.city_department:
                name += f"{record.city_department:02}"
            if record.zone_or_session_cad:
                name += f"{separator}{record.zone_or_session_cad:02}"
            if record.quarter_number:
                name += f"{separator}{record.quarter_number:02}"
            if record.installment_lot_number:
                name += f"{separator}{record.installment_lot_number:02}"
            if record.sub_installment_number:
                name += f"{separator}{record.sub_installment_number:04}"
            record.name = name