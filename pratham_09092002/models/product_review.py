# -*- coding: utf-8 -*-

from odoo import models, fields,api


class ProductReview(models.Model):
    _name = 'product.review'
    """
    Create custom model to perform some operation.
    """
    #fields
    product_id = fields.Many2one('product.template', string='Product')
    user_id = fields.Many2one('res.users', string='User')
    rating = fields.Selection([
        ('1', 'Very Low'),
        ('2', 'Low'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Very Good')], string='Rating'
    )
    description = fields.Text(string='Review', required=True)
    create_date = fields.Datetime(string='Submitted On', readonly=True)
    reviewer_name = fields.Char(string='Reviewer Name', compute='_compute_reviewer_name')

    @api.depends('user_id')
    def _compute_reviewer_name(self):
        """
        This method is created for display reviewer name.
        """
        for review in self:
            if review.user_id and review.user_id.partner_id and review.user_id.partner_id.name:
                review.reviewer_name = review.user_id.partner_id.name
            else:
                review.reviewer_name = "Anonymous"
