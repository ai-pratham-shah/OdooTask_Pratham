# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    """
    Inherits sale.order and adds custom approval logic
    for orders containing products with low stock.
    """
    _inherit = 'sale.order'

    approval_needed = fields.Boolean('Approval Needed', default=False)
    is_check = fields.Boolean(default=False)

    def action_confirm(self):
        """
        Confirms the sale order. If any product in the order has a stock quantity
        of less than 5, approval is required before confirming.

        Returns:
            dict | None: If approval is required, returns an action to open an approval wizard.
                         Otherwise, proceeds with the standard confirmation.
        """
        # Orders that can be confirmed directly
        to_confirm = self.filtered(lambda order: order.is_check)

        # Orders that require approval check
        to_approve = self - to_confirm

        approval_orders = []
        for order in to_approve:
            low_stock_books = [
                line.product_id.name for line in order.order_line
                if line.product_id.qty_available < 5
            ]
            if low_stock_books:
                message = f"Approval needed! The following books have low stock: {', '.join(low_stock_books)}"
                order.approval_needed = True
                approval_orders.append((order.id, message))

        if approval_orders:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.approval.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_message': approval_orders[0][1]}  # Show message for the first order
            }

        return super().action_confirm()

    def action_approve(self):
        """
        Approves the sale order. Only a manager can approve orders.
        This action removes the approval flag and allows order confirmation.

        Returns:
            None
        """
        if self.env.user.is_manager:
            self.filtered(lambda order: order.approval_needed).write({
                'approval_needed': False,
                'is_check': True
            })

    def action_reject(self):
        """
        Rejects the sale order. Only a manager can reject orders.
        This action removes the approval flag and cancels the order.

        Returns:
            dict: Result of the `action_cancel` method.
        """
        self.write({'approval_needed': False})
        return super().action_cancel()

    def action_cancel(self):
        """
        Cancels the sale order. If the order was previously approved,
        it resets the `is_check` flag before canceling.

        Returns:
            dict: Result of the `super().action_cancel()` method.
        """
        self.filtered(lambda order: order.is_check).write({'is_check': False})
        return super().action_cancel()
