# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp

class HrSalaryRule(models.Model):
    _inherit = ['hr.salary.rule']

    #TODO should add some checks on the type of result (should be float)
    @api.multi
    def _compute_rule(self, localdict):
        """
        :param localdict: dictionary containing the environement in which to compute the rule
        :return: returns a tuple build as the base/amount computed, the quantity and the rate
        :rtype: (float, float, float)
        """
        self.ensure_one()
        if self.amount_select == 'fix':
            try:
                return self.amount_fix, float(safe_eval(self.quantity, localdict)), 100.0
            except Exception as e:
                raise UserError(_('Wrong quantity defined for salary rule %s (%s). Error: %s.') % (self.name, self.code, e))
        elif self.amount_select == 'percentage':
            try:
                return (float(safe_eval(self.amount_percentage_base, localdict)),
                        float(safe_eval(self.quantity, localdict)),
                        self.amount_percentage)
            except Exception as e:
                raise UserError(_('Wrong percentage base or quantity defined for salary rule %s (%s). Error: %s.') % (self.name, self.code, e))
        else:
            try:
                safe_eval(self.amount_python_compute, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), 'result_qty' in localdict and localdict['result_qty'] or 1.0, 'result_rate' in localdict and localdict['result_rate'] or 100.0
            except Exception as e:
                raise UserError(_('Wrong python code defined for salary rule %s (%s). Error: %s.') % (self.name, self.code, e))

    @api.multi
    def _satisfy_condition(self, localdict):
        """
        @param contract_id: id of hr.contract to be tested
        @return: returns True if the given rule match the condition for the given contract. Return False otherwise.
        """
        self.ensure_one()

        if self.condition_select == 'none':
            return True
        elif self.condition_select == 'range':
            try:
                result = safe_eval(self.condition_range, localdict)
                return self.condition_range_min <= result and result <= self.condition_range_max or False
            except Exception as e:
                raise UserError(_('Wrong range condition defined for salary rule %s (%s). Error: %s.') % (self.name, self.code, e))
        else:  # python code
            try:
                safe_eval(self.condition_python, localdict, mode='exec', nocopy=True)
                return 'result' in localdict and localdict['result'] or False
            except Exception as e:
                raise UserError(_('Wrong python condition defined for salary rule %s (%s). Error: %s.') % (self.name, self.code, e))
