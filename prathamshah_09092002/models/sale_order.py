# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    """
    This model is created for perform some approval related operation
    """

    approval_required = fields.Boolean(string='Approval Required', default=False)
    approval_state = fields.Selection([
        ('to_submit', 'To Submit'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved')
    ], string='Approval Status', default='to_submit')
    approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Datetime(string='Approved Date', readonly=True)
    approver_id = fields.Many2one('res.users', string='Assigned Approver', copy=False)

    def _get_appropriate_approver(self):
        """Get the appropriate approver based on the order amount."""
        if not self.company_id.sales_approval_threshold_ids:
            return False

        # Get threshold configurations in ascending order
        thresholds = self.company_id.sales_approval_threshold_ids.filtered(
            lambda t: t.currency_id == self.currency_id
        ).sorted(key=lambda t: t.approval_threshold)

        if not thresholds:
            return False

        # Find the appropriate approver
        for threshold in thresholds:
            if self.amount_total <= threshold.approval_threshold:
                return threshold.sales_manager_id

        # If amount exceeds all thresholds, use the highest threshold's manager
        if thresholds:
            return thresholds[-1].sales_manager_id

        return False

    def _check_approval_required(self):
        """Check if the order requires approval based on threshold."""
        if self.state in ('draft', 'sent'):
            thresholds = self.company_id.sales_approval_threshold_ids.filtered(
                lambda t: t.currency_id == self.currency_id
            ).sorted(key=lambda t: t.approval_threshold)

            if not thresholds:
                self.approval_required = False
                return

            # Find the lowest threshold
            lowest_threshold = thresholds[0] if thresholds else False

            if lowest_threshold and self.amount_total >= lowest_threshold.approval_threshold:
                self.approval_required = True
                self.approver_id = self._get_appropriate_approver()
            else:
                self.approval_required = False
                self.approver_id = False

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """Override to check approval requirement when total changes."""
        res = super(SaleOrder, self)._amount_all()
        for order in self:
            order._check_approval_required()
        return res

    def action_confirm(self):
        """Override to check if approval is needed before confirmation."""
        for order in self:
            if order.approval_required and order.approval_state != 'approved':
                raise ValidationError(_("This order requires "
                                        "approval before confirmation."))
        return super(SaleOrder, self).action_confirm()

    def action_send_for_approval(self):
        """Send the order for approval."""
        self.ensure_one()
        if not self.approver_id:
            self.approver_id = self._get_appropriate_approver()

        self.approval_state = 'pending_approval'

        # Log in chatter
        threshold_record = self.company_id.sales_approval_threshold_ids.filtered(
            lambda t: t.sales_manager_id == self.approver_id
                      and t.currency_id == self.currency_id
        )
        threshold_amount = threshold_record.approval_threshold if threshold_record else 0

        msg = _("""Order sent for approval:
        - Total Amount: %s %s
        - Threshold: %s %s
        - Assigned Approver: %s""") % (
            self.currency_id.symbol, self.amount_total,
            self.currency_id.symbol, threshold_amount,
            self.approver_id.name
        )
        self.message_post(body=msg)

        # Send email notification
        template = self.env.ref('prathamshah_09092002.'
                                'email_template_sale_approval')
        if template:
            template.send_mail(self.id, force_send=True)

        return True

    def action_approve_order(self):
        """Approve the sales order."""
        self.ensure_one()
        if self.approval_state != 'pending_approval':
            raise ValidationError(_("This order is not pending approval."))

        # Check if current user is allowed to approve
        current_user = self.env.user
        if (current_user.id != self.approver_id.id and
                not current_user.has_group('sales_team.group_sale_manager')):
            raise ValidationError(_("You are not authorized to approve this order."))

        self.approval_state = 'approved'
        self.approved_by_id = current_user.id
        self.approved_date = fields.Datetime.now()

        # Log in chatter
        msg = _("""Order approved by %s on %s""") % (
            current_user.name,
            fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.message_post(body=msg)
        # Confirm the order
        super(SaleOrder, self).action_confirm()
        return True

    def write(self, vals):
        """Override to trigger re-approval if amount changes."""
        result = super(SaleOrder, self).write(vals)

        # If order_line changes and order is already approved, check if re-approval is needed
        if 'order_line' in vals and self.approval_state == 'approved':
            for order in self:
                order._check_approval_required()
                if order.approval_required:
                    order.approval_state = 'to_submit'

                    # Log in chatter
                    msg = _("Order modified - re-approval required.")
                    order.message_post(body=msg)

        return result

    def send_approval_reminders(self):
        """Send reminder emails for pending approval orders."""
        pending_orders = self.env['sale.order'].search([
            ('approval_state', '=', 'pending_approval'),
            ('approver_id', '!=', False)
        ])
        if not pending_orders:
            return True
        # Group orders by approver
        orders_by_approver = {}
        for order in pending_orders:
            if order.approver_id.id not in orders_by_approver:
                orders_by_approver[order.approver_id.id] = []
            orders_by_approver[order.approver_id.id].append(order)

        # Get the reminder email template
        template = self.env.ref('prathamshah_09092002.'
                                'email_template_sale_approval_reminder')
        if not template:
            raise ValidationError(_("Reminder email template not found!"))
        # Send reminders
        for approver_id, orders in orders_by_approver.items():
            approver = self.env['res.users'].browse(approver_id)
            if not approver.exists():
                continue
            # Create context with orders for the template
            for order in orders:
                order_list = (f"Order {order.name} - "
                              f"{order.currency_id.symbol}{order.amount_total:.2f}")
            # Send email
            template.with_context(order_list=order_list).send_mail(
                orders[0].id,
                email_values={'recipient_ids': [(6, 0, [approver.partner_id.id])]},
                force_send=True
            )

        return True



