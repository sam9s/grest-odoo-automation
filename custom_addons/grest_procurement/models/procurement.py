# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class GrestProcurement(models.Model):
    _name = 'grest.procurement'
    _description = 'GREST Device Procurement'
    _order = 'serial_number desc'
    _rec_name = 'name'

    # ========== BASIC INFORMATION ==========
    serial_number = fields.Integer(
        string='Serial Number',
        readonly=True,
        copy=False,
        index=True
    )

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
        readonly=True
    )

    purchase_date = fields.Date(
        string='Purchase Date',
        required=True,
        default=fields.Date.today,
        index=True
    )

    purchase_month = fields.Char(
        string='Purchase Month',
        compute='_compute_purchase_month',
        store=True,
        readonly=True
    )

    technician_id = fields.Many2one(
        'res.users',
        string='Technician',
        required=True,
        default=lambda self: self.env.user,
        index=True
    )

    # ========== DEVICE INFORMATION ==========
    category = fields.Selection([
        ('mobile', 'Mobile'),
        ('tab', 'Tab'),
        ('laptop', 'Laptop'),
        ('watch', 'Watch'),
        ('airpods', 'Airpods'),
    ], string='Category', required=True, index=True)

    imei = fields.Char(
        string='IMEI Number',
        required=True,
        index=True,
        copy=False
    )

    model_id = fields.Many2one(
        'product.product',
        string='Model',
        required=True,
        index=True
    )

    brand = fields.Char(
        string='Brand',
        related='model_id.product_tmpl_id.brand',
        store=True,
        readonly=True
    )

    ram = fields.Char(
        string='RAM',
        related='model_id.product_tmpl_id.ram',
        store=True,
        readonly=True
    )

    rom = fields.Char(
        string='ROM',
        related='model_id.product_tmpl_id.rom',
        store=True,
        readonly=True
    )

    # ========== SOURCE INFORMATION ==========
    source_name = fields.Selection([
        ('cashify_b2b', 'Cashify B2B'),
        ('cashify_trading', 'Cashify Trading'),
        ('unicorn', 'Unicorn'),
        ('sangeeta', 'Sangeeta'),
        ('trade_in', 'Trade-In'),
        ('other', 'Other'),
    ], string='Source', required=True, index=True)

    store_name = fields.Char(
        string='Store Name'
    )

    # ========== PRICING ==========
    price_offered = fields.Float(
        string='Price Offered to Customer',
        required=True,
        digits=(16, 2)
    )

    ave_price = fields.Float(
        string='Average Price',
        digits=(16, 2)
    )

    logistic_charge = fields.Float(
        string='Logistic Charge',
        default=0.0,
        digits=(16, 2)
    )

    extra_amount = fields.Float(
        string='Extra Amount Given',
        default=0.0,
        digits=(16, 2),
        help='Extra amount if customer negotiated'
    )

    credit_used = fields.Float(
        string='Credit Used',
        default=0.0,
        digits=(16, 2),
        help='Partner credit points used'
    )

    commission_amount = fields.Float(
        string='Commission Amount',
        compute='_compute_pricing',
        store=True,
        readonly=True,
        digits=(16, 2)
    )

    purchase_price_no_commission = fields.Float(
        string='Purchase Price (No Commission)',
        compute='_compute_pricing',
        store=True,
        readonly=True,
        digits=(16, 2)
    )

    total_price = fields.Float(
        string='Total Price',
        compute='_compute_pricing',
        store=True,
        readonly=True,
        digits=(16, 2)
    )

    # ========== GSN GENERATION ==========
    gsn = fields.Char(
        string='GSN Barcode',
        compute='_compute_gsn',
        store=True,
        readonly=True,
        index=True,
        copy=False
    )

    # NOTE: grest_unique_code is a mirror of gsn via related — no manual writes needed
    grest_unique_code = fields.Char(
        string='GREST Unique Code',
        related='gsn',
        store=True,
        readonly=True
    )

    # ========== PAYMENT TRACKING ==========
    payment_scenario = fields.Selection([
        ('paid', 'Fully Paid'),
        ('partial', 'Partially Paid'),
        ('credit', 'Credit Note'),
    ], string='Payment Scenario', required=True, default='paid')

    payment_status = fields.Char(
        string='Payment Status'
    )

    payment_date = fields.Date(
        string='Payment Date'
    )

    payment_month = fields.Char(
        string='Payment Month',
        compute='_compute_payment_month',
        store=True,
        readonly=True
    )

    payment_utr = fields.Char(
        string='Payment UTR Number'
    )

    # ========== RECEIVING ==========
    grest_received = fields.Boolean(
        string='GREST Received',
        default=False
    )

    receiving_date = fields.Date(
        string='Receiving Date'
    )

    receiving_month = fields.Char(
        string='Receiving Month',
        compute='_compute_receiving_month',
        store=True,
        readonly=True
    )

    # ========== HANDOVER ==========
    handover_date = fields.Date(
        string='Handover Date'
    )

    handover_month = fields.Char(
        string='Handover Month',
        compute='_compute_handover_month',
        store=True,
        readonly=True
    )

    # ========== STATUS & GRADING ==========
    grade = fields.Char(string='Grade')
    els_grade = fields.Char(string='ELS Grade')

    status = fields.Selection([
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('handed_over', 'Handed Over'),
    ], string='Status', default='pending', index=True)

    due_amount = fields.Float(
        string='Due Amount',
        default=0.0,
        digits=(16, 2)
    )

    amount_balance = fields.Float(
        string='Amount Balance',
        default=0.0,
        digits=(16, 2)
    )

    # ========== COMMISSION PAYMENT ==========
    commission_payment_status = fields.Char(string='Commission Payment Status')
    commission_utr = fields.Char(string='Commission UTR')
    commission_paid_date = fields.Date(string='Commission Paid Date')

    # ========== INVOICE & APPROVAL ==========
    invoice_file = fields.Binary(
        string='Invoice File',
        attachment=True
    )

    invoice_filename = fields.Char(string='Invoice Filename')

    approval_status = fields.Selection([
        ('pending', 'Pending Accounts Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected by Accounts'),
    ], string='Approval Status', default='pending', readonly=True, index=True)

    # NOTE: approval records are in grest_accounts_approval module.
    # They link back here via procurement_id on grest.accounts.approval.
    # View them in Accounts → Dashboard.

    # ========== FUTURE FIELDS (PHASE 3) ==========
    price_with_spare = fields.Float(string='Price With Spare', digits=(16, 2))
    final_price = fields.Float(string='Final Price', digits=(16, 2))
    sales_price = fields.Float(string='Sales Price', digits=(16, 2))
    p_and_l = fields.Float(string='P&L', digits=(16, 2))

    # ========== COMPUTED FIELDS ==========

    @api.depends('serial_number')
    def _compute_name(self):
        """Generate display name"""
        for record in self:
            if record.serial_number:
                record.name = f"PROC-{record.serial_number}"
            else:
                record.name = 'New'

    @api.depends('purchase_date')
    def _compute_purchase_month(self):
        """Auto-generate month from purchase date"""
        for record in self:
            if record.purchase_date:
                record.purchase_month = record.purchase_date.strftime('%b_%Y')
            else:
                record.purchase_month = ''

    @api.depends('payment_date')
    def _compute_payment_month(self):
        """Auto-generate month from payment date"""
        for record in self:
            if record.payment_date:
                record.payment_month = record.payment_date.strftime('%b_%Y')
            else:
                record.payment_month = ''

    @api.depends('receiving_date')
    def _compute_receiving_month(self):
        """Auto-generate month from receiving date"""
        for record in self:
            if record.receiving_date:
                record.receiving_month = record.receiving_date.strftime('%b_%Y')
            else:
                record.receiving_month = ''

    @api.depends('handover_date')
    def _compute_handover_month(self):
        """Auto-generate month from handover date"""
        for record in self:
            if record.handover_date:
                record.handover_month = record.handover_date.strftime('%b_%Y')
            else:
                record.handover_month = ''

    @api.depends('source_name', 'imei', 'technician_id', 'serial_number', 'purchase_month')
    def _compute_gsn(self):
        """
        Generate unique GSN barcode.

        TEMPORARY FORMULA - WILL BE UPDATED BY WAREHOUSE TEAM (Nikhil)

        Format: GRG + Source(3) + IMEI(last4) + Tech(4) + Serial(2-padded) + Month(1char)
        Example: GRGUNI6245SAUR01N
          GRG  = fixed prefix
          UNI  = Unicorn
          6245 = last 4 digits of IMEI (356281920626245 → 6245)
          SAUR = first 4 chars of technician name
          01   = serial number, zero-padded to 2 digits
          N    = first char of month (Nov_2025 → N)

        TODO: Replace with actual warehouse formula when Nikhil provides it.
        """
        SOURCE_CODES = {
            'cashify_b2b': 'CAS',
            'cashify_trading': 'CAT',
            'unicorn': 'UNI',
            'sangeeta': 'SAN',
            'trade_in': 'TRA',
            'other': 'OTH',
        }

        for record in self:
            if all([record.source_name, record.imei, record.technician_id,
                    record.serial_number, record.purchase_month]):

                source_code = SOURCE_CODES.get(record.source_name, 'OTH')

                # IMEI: last 4 digits  (FIX: was incorrectly [-5:] in Astra's version)
                imei_str = str(record.imei).replace('.', '').replace(' ', '')
                imei_last4 = imei_str[-4:] if len(imei_str) >= 4 else imei_str.zfill(4)

                # Technician: first 4 uppercase chars, padded with X if name is short
                tech_name = record.technician_id.name or 'UNKN'
                tech_code = tech_name[:4].upper().ljust(4, 'X')

                # Serial: 2 digits, zero-padded (e.g. 1 → 01, 99 → 99)
                serial_str = str(record.serial_number).zfill(2)[-2:]

                # Month: first char uppercase (Nov_2025 → N)
                month_first = record.purchase_month[:1].upper() if record.purchase_month else 'X'

                record.gsn = f"GRG{source_code}{imei_last4}{tech_code}{serial_str}{month_first}"
            else:
                record.gsn = ''

    @api.depends('price_offered', 'source_name', 'logistic_charge', 'extra_amount')
    def _compute_pricing(self):
        """
        Calculate commission and total price.

        Commission rates by source:
          Cashify B2B:      0%  (no commission)
          Cashify Trading:  0%  (variable, manual entry)
          Unicorn:         12%
          Sangeeta:        12%
          Trade-in:        10%
          Other:           12%

        Formula: total = (price_offered + extra_amount) * (1 + rate) + logistic_charge
        """
        COMMISSION_RATES = {
            'cashify_b2b': 0.00,
            'cashify_trading': 0.00,
            'unicorn': 0.12,
            'sangeeta': 0.12,
            'trade_in': 0.10,
            'other': 0.12,
        }

        for record in self:
            rate = COMMISSION_RATES.get(record.source_name, 0.12)
            base = record.price_offered + record.extra_amount
            record.commission_amount = base * rate
            record.purchase_price_no_commission = base
            record.total_price = (base * (1 + rate)) + record.logistic_charge

    # ========== CRUD ==========

    @api.model
    def create(self, vals):
        """Auto-generate serial number and create linked accounts approval record."""
        last = self.search([], order='serial_number desc', limit=1)
        vals['serial_number'] = (last.serial_number + 1) if last else 1

        record = super(GrestProcurement, self).create(vals)

        # Auto-create approval — wrapped safely in case accounts module not yet installed
        if 'grest.accounts.approval' in self.env:
            self.env['grest.accounts.approval'].create({
                'procurement_id': record.id,
                'payment_scenario': record.payment_scenario,
                'state': 'pending',
                'payment_status': 'pending',
            })

        return record

    # ========== CONSTRAINTS ==========

    @api.constrains('imei')
    def _check_imei_unique(self):
        """Ensure IMEI is unique across all procurement records."""
        for record in self:
            if record.imei:
                duplicate = self.search([
                    ('imei', '=', record.imei),
                    ('id', '!=', record.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        f"IMEI {record.imei} already exists in record {duplicate.name}"
                    )

    @api.constrains('gsn')
    def _check_gsn_unique(self):
        """Ensure GSN is unique across all procurement records."""
        for record in self:
            if record.gsn:
                duplicate = self.search([
                    ('gsn', '=', record.gsn),
                    ('id', '!=', record.id)
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        f"GSN {record.gsn} already exists in record {duplicate.name}"
                    )
