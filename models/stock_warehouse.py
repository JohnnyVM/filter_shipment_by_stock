# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
    Add the field many to one to shipping
"""

import logging

from decimal import Decimal

from odoo import api, models, fields, http

_logger = logging.getLogger(__name__)

class Warehouse(models.Model):
    """ Sabadell Model class """
    _inherit = "stock.warehouse"

    description = "Add delivery field"
