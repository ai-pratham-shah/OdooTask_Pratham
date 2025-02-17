# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # Check if any book has stock less than 5
        low_stock_books = []
        for line in self.order_line:
            product = line.product_id
            print(product.qty_available)
            if product.qty_available < 5:
                low_stock_books.append(product.name)

        if low_stock_books:
            # Show dynamic warning message
            message = f"Approval needed! The following books have low stock: {', '.join(low_stock_books)}"
            raise UserError(message)

        # Proceed with the base confirm action if no low stock
        return super().action_confirm()

    def action_approve(self):
        """ Approve the order (Manager only) """
        if not self.env.user.is_manager:
            print(self.env.user.is_manager)
            raise UserError("You need to be a Manager to approve the order.")

        # Re-enable the confirm button
        self.state = 'sale'
        return True

    def action_reject(self):
        pass