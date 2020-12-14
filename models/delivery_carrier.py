# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
    Add the field one to many to warehouse
"""

import logging

from decimal import Decimal

from odoo import api, models, fields, http

_logger = logging.getLogger(__name__)

class Delivery(models.Model):
    """ Sabadell Model class """
    _inherit = "delivery.carrier"

    description = "Add warehouse filter"

    stock_warehouse_ids = fields.Many2many("stock.warehouse")
