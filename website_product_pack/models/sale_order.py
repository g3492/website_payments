##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(
        self, product_id=None,
            line_id=None, add_qty=0, set_qty=0, **kwargs):
        sale_order_line = self.env['sale.order.line'].browse(line_id)
        if sale_order_line.pack_parent_line_id:
            return {
                'line_id': line_id,
                'quantity': sale_order_line.product_uom_qty}
        return super(SaleOrder, self)._cart_update(
            product_id=product_id, line_id=line_id,
            add_qty=add_qty, set_qty=set_qty, **kwargs)

    @api.multi
    def _cart_find_product_line(self, product_id=None, line_id=None, **kwargs):
        """ the function is not very inheritable, we can grab these
        results and look over them but this would make them run two sql
        line_ids = super(SaleOrder, self)._cart_find_product_line(
            cr, uid, ids, product_id=product_id, line_id=line_id,
            context=context, **kwargs)
        """
        for so in self:
            domain = [('order_id', '=', so.id),
                      ('product_id', '=', product_id),
                      ('pack_parent_line_id', '=', False)]
            if line_id:
                domain += [('id', '=', line_id)]
            return self.env['sale.order.line'].sudo().search(domain)
