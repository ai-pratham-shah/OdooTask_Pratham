# -*- coding: utf-8 -*-

from odoo import models, fields
class SaleOrder(models.Model):
    """
    Inherit sale order and add some custom buttons
    """
    _inherit = 'sale.order'

    approval_needed = fields.Boolean('Approval Needed', default=False)
    is_check  = fields.Boolean(default=False)

    def action_confirm(self):
        """
        This function checks if the selected product
        quantity is less than 5 or not.
        """
        # Check if any book has stock less than 5
        if self.is_check:
            return super().action_confirm()

        low_stock_books = []
        for line in self.order_line:
            product = line.product_id
            if product.qty_available < 5:
                low_stock_books.append(product.name)
        if low_stock_books:
            # Create the dynamic message
            message = (f"Approval needed! The following books have low stock: "
                       f"{', '.join(low_stock_books)}")
            self.write({'approval_needed': True})
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.approval.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_message': message
                }
            }
        return super().action_confirm()

    def action_approve(self):
        """ Approve the order (Manager only) """
        if self.env.user.is_manager:
            self.write({'approval_needed': False})
            self.write({'is_check' : True})

    def action_reject(self):
        """ Reject the order (Manager only) """
        self.write({'approval_needed': False})
        return super().action_cancel()

    def action_cancel(self):
        """ Cancel the order """
        if self.is_check:
            self.write({'is_check' : False})
        return super().action_cancel()