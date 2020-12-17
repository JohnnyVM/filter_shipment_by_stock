# -*- coding: utf-8 -*-

"""
    Override the shipping methods output
"""

import logging

from odoo import models

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_methods(self):
        """
        Remove shipping methods if warehouse defined and stock no available
        """
        def __miss_qty(asked: dict, available: dict) -> list:
            """ List with the missing product """
            missing = []
            for key in asked.keys():
                if asked[key] > available.get(key, 0):
                    missing.append(key)
            return missing

        delivery_methods = super(SaleOrder, self)._get_delivery_methods()

        # No warehouse defined
        no_warehouse = delivery_methods.filtered('stock_warehouse_ids')
        if not no_warehouse:
            return delivery_methods

        # get the product qty in the order
        order_line = self.order_line.filtered(
            lambda x: (not x.is_delivery) and x.product_id.product_tmpl_id.type == 'product'
        )
        order_qty = dict(zip(
            order_line.mapped('product_id.id'),
            order_line.mapped('product_qty')
        ))

        warehouse_qty = dict()
        discart = self.env['delivery.carrier']
        delivery_warehouse = delivery_methods - no_warehouse
        for shipping in delivery_warehouse:
            stock_location = self.env['stock.quant'].search([
                ('location_id', 'in', shipping.stock_warehouse_ids.lot_stock_id.ids),
                ('product_id', 'in', order_line.mapped('product_id.id'))
            ])
            for product in order_line.mapped('product_id'):
                warehouse_qty[product.id] = \
                        sum(stock_location.filtered(lambda x: x.product_id == product.id).mapped('available_quantity'))

            missing_stock = __miss_qty(order_qty, warehouse_qty)
            if missing_stock:
                _logger.info(
                        "Order: %s. Shipping: %s discarted. Missing products: %s",
                        self.name,
                        shipping.name,
                        missing_stock
                )
                discart += shipping

        return no_warehouse + (delivery_warehouse - discart)
