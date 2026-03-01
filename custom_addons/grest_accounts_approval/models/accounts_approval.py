# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class GrestAccountsApproval(models.Model):
    _name = 'grest.accounts.approval'
    _description = 'Accounts Approval Workflow'
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
        readonly=True
    )

    procurement_id = fields.Many2one(
        'grest.procurement',
        string='Procurement',
        required=True,
        ondelete='cascade',
        index=True
    )

    # ── Related read-only fields from procurement ─────────────────────────────
    gsn = fields.Char(
        string='GSN',
        related='procurement_id.gsn',
        store=True,
        readonly=True
    )

    imei = fields.Char(
        string='IMEI',
        related='procurement_id.imei',
        readonly=True
    )

    model_id = fields.Many2one(
        'product.product',
        string='Model',
        related='procurement_id.model_id',
        readonly=True
    )

    source_name = fields.Selection(
        string='Source',
        related='procurement_id.source_name',
        readonly=True
    )

    price_offered = fields.Float(
        string='Price Offered',
        related='procurement_id.price_offered',
        readonly=True
    )

    total_price = fields.Float(
        string='Total Price',
        related='procurement_id.total_price',
        readonly=True
    )

    invoice_file = fields.Binary(
        string='Invoice',
        related='procurement_id.invoice_file',
        readonly=True
    )

    invoice_filename = fields.Char(
        string='Invoice Filename',
        related='procurement_id.invoice_filename',
        readonly=True
    )

    payment_scenario = fields.Selection(
        string='Payment Scenario',
        related='procurement_id.payment_scenario',
        readonly=True
    )

    # ── Approval-specific fields ──────────────────────────────────────────────
    payment_status = fields.Selection([
        ('pending', 'Pending Review'),
        ('verified', 'Payment Verified'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Payment Status', required=True, default='pending')

    payment_utr = fields.Char(string='Payment UTR')
    credit_days = fields.Integer(string='Credit Days')
    partial_amount = fields.Float(string='Partial Amount Paid', digits=(16, 2))

    approval_date = fields.Datetime(string='Approval Date', readonly=True)
    approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True)

    rejection_reason = fields.Text(string='Rejection Reason')
    notes = fields.Text(string='Notes')

    state = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='State', default='pending', required=True, index=True)

    # ── Computed ──────────────────────────────────────────────────────────────

    @api.depends('procurement_id', 'procurement_id.name')
    def _compute_name(self):
        for record in self:
            if record.procurement_id:
                record.name = f"APPR-{record.procurement_id.name}"
            else:
                record.name = 'New'

    # ── Actions ───────────────────────────────────────────────────────────────

    def action_approve(self):
        """Approve the procurement — sets state, stamps approver and date."""
        for record in self:
            record.write({
                'state': 'approved',
                'payment_status': 'approved',
                'approval_date': fields.Datetime.now(),
                'approved_by_id': self.env.user.id,
            })
            record.procurement_id.write({'approval_status': 'approved'})
        return True

    def action_reject(self):
        """Reject the procurement — requires a rejection reason."""
        for record in self:
            if not record.rejection_reason:
                raise UserError(_("Please provide a rejection reason before rejecting."))
            record.write({
                'state': 'rejected',
                'payment_status': 'rejected',
            })
            record.procurement_id.write({'approval_status': 'rejected'})
        return True
