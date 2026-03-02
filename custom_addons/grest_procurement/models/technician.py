# -*- coding: utf-8 -*-
from odoo import models, fields


class GrestTechnician(models.Model):
    """
    GREST Technician master list.

    Separate from res.users — technicians do not need Odoo login accounts.
    Pre-populated with 24 names from the Procurement Sample Sheet.
    """
    _name = 'grest.technician'
    _description = 'GREST Technician'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(
        string='Technician Name',
        required=True,
        index=True
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Uncheck to hide without deleting'
    )
