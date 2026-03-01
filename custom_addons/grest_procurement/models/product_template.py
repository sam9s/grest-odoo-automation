# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """
    Inherit product.template to add custom fields for device specifications.

    Fields added:
    - brand: Device manufacturer (Apple, Samsung, OnePlus, etc.)
    - ram:   RAM specification (4GB, 6GB, 8GB, etc.)
    - rom:   Storage capacity (64GB, 128GB, 256GB, etc.)
    """
    _inherit = 'product.template'

    brand = fields.Char(
        string='Brand',
        help='Device brand/manufacturer (e.g., Apple, Samsung, OnePlus)',
        index=True
    )

    ram = fields.Char(
        string='RAM',
        help='RAM specification (e.g., 4GB, 6GB, 8GB)'
    )

    rom = fields.Char(
        string='Storage',
        help='Storage capacity (e.g., 64GB, 128GB, 256GB)'
    )
