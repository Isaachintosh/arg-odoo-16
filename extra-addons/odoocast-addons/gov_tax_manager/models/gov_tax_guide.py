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
    
    account_move_id = fields.Many2one(
        comodel_name='account.move',
        string="Fatura"
    )
    
    status = fields.Selection([
        ('draft', 'Borrador'),
        ('validate', 'Validado'),
        ('generated', 'Gerado'),
        ('paid', 'Pago'),
        ('cancelled', 'Cancelado')
    ], string="Situación", default='draft')
    
    @api.depends('property_id', 'tax_rate_id')
    @api.onchange('property_id', 'tax_rate_id')
    def compute_tax_amount(self):
        for record in self:
            tax_amount = 0
            if record.tax_rate_id:
                tax_line_id = record.tax_rate_id.tax_line_ids.search([
                    ('min_value', '<=', record.property_id.fiscal_building_value),
                    ('max_value', '>=', record.property_id.fiscal_building_value)
                ], limit=1)
                if tax_line_id:
                    tax_amount = round(record.property_id.fiscal_building_value * tax_line_id.tax_rate, 2)
            record.tax_amount = tax_amount

    def action_validate(self):
        for record in self:
            if record.status == 'draft':
                record.status = 'validate'

    def action_cancel(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError(_('Guia de pagamento já cancelada.'))
            if record.status == 'generated':
                raise UserError(_('Guia de pagamento já gerada. Cancele a Factura antes.'))
            record.status = 'cancelled'

    def action_generate_invoice(self):
        for record in self:
            if record.status == 'generated':
                raise UserError(_('Factura já gerada.'))
            if record.status != 'validate':
                raise UserError(_('Guia de pagamento não validada. Favor revisionar.'))
            record.status = 'generated'
            record.invoice_date = fields.Date.today()
            account_move_id = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.owner_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [
                    (0, 0, {
                        'name': record.tax_rate_id.name,
                        'quantity': 1,
                        'price_unit': record.tax_amount,
                    })
                ]
            })
            if account_move_id:
                record.account_move_id = account_move_id
