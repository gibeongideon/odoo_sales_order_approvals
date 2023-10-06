from odoo import models, fields, api

class SoApproval(models.Model):
    _inherit = "sale.order"

    button_visibility = fields.Boolean(string="Approve button")
    state = fields.Selection(selection_add=[('waiting', 'Waiting for Approval')
                                            ], string='Status', readonly=True
                             )

    @api.onchange("order_line")
    def approval(self):
        for record in self.order_line:
            if record.price_unit < record.product_template_id.list_price or \
                    record.price_unit > record.product_template_id.list_price:
                self.write({'button_visibility': True})
                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'You need Approval from manager'
                    }
                }


    def button_manager(self):
        self.write({'state': 'waiting'})


    def button_approve(self):
        self.write({'state': 'sent'})
        return self.action_quotation_send()
        

    def button_reject(self):
        self.write({'state': 'draft'})
