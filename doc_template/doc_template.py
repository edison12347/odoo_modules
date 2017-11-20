# -*- coding: utf-8 -*-
"""
Accounting Documents template

"""

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import datetime

import time
import logging

_logger = logging.getLogger(__name__)


class Primary_documentation(models.Model):
    _name = 'document.template'
    # _inherit = "wizard.select.move.template"

    date = fields.Date('Date')
    partner_id = fields.Many2one('res.partner', 'Agent')
    template_id = fields.Many2one('account.move.template')
    amount = fields.Float('Amount')

    @api.multi
    def over_the_wizard(self):
        self.ensure_one()
        account_period_model = self.env['account.period']
        # if not self.check_zero_lines():
        #     raise exceptions.Warning(
        #         _('At least one amount has to be non-zero!')
        #     )
        _logger.info('!!!!!!!!!!!!!!______state_________!!!!!!!!!!! ')
        input_lines = {}
        _logger.info('!!!!!!!!!!!!!!______line_ids_________!!!!!!!!!!! ')
        for template_line in self.template_id.template_line_ids:
            if template_line.type == 'input':
                input_lines[template_line.sequence] = self.amount
                _logger.info('!!!!!!!!!!!!!!______template_line_________!!!!!!!!!!! %s', template_line)
        period = account_period_model.find()
        if not period:
            raise exceptions.Warning(_('Unable to find a valid period !'))

        computed_lines = self.template_id.compute_lines(input_lines)

        moves = {}
        for line in self.template_id.template_line_ids:
            if line.journal_id.id not in moves:
                moves[line.journal_id.id] = self._make_move(
                    self.template_id.name,
                    period.id,
                    line.journal_id.id,
                    self.partner_id.id
                )

            self._make_move_line(
                line,
                computed_lines,
                moves[line.journal_id.id],
                period.id,
                self.partner_id.id
            )
            if self.template_id.cross_journals:
                trans_account_id = self.template_id.transitory_acc_id.id
                self._make_transitory_move_line(
                    line,
                    computed_lines,
                    moves[line.journal_id.id],
                    period.id,
                    trans_account_id,
                    self.partner_id.id
                )

        return {
            'domain': "[('id','in', " + str(moves.values()) + ")]",
            'name': 'Entries',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    @api.model
    def _make_move(self, ref, period_id, journal_id, partner_id):
        move = self.env['account.move'].create({
            'ref': ref,
            'period_id': period_id,
            'journal_id': journal_id,
            'partner_id': partner_id,
        })
        return move.id

    @api.model
    def _make_move_line(self, line, computed_lines,
                        move_id, period_id, partner_id):
        account_move_line_model = self.env['account.move.line']
        analytic_account_id = False
        if line.analytic_account_id:
            if not line.journal_id.analytic_journal_id:
                raise exceptions.Warning(
                    _("You have to define an analytic "
                      "journal on the '%s' journal!")
                    % (line.journal_id.name,)
                )

            analytic_account_id = line.analytic_account_id.id
        vals = {
            'name': line.name,
            'move_id': move_id,
            'journal_id': line.journal_id.id,
            'period_id': period_id,
            'analytic_account_id': analytic_account_id,
            'account_id': line.account_id.id,
            'date': time.strftime('%Y-%m-%d'),
            'account_tax_id': line.account_tax_id.id,
            'credit': 0.0,
            'debit': 0.0,
            'partner_id': partner_id,
        }
        if line.move_line_type == 'cr':
            vals['credit'] = computed_lines[line.sequence]
        if line.move_line_type == 'dr':
            vals['debit'] = computed_lines[line.sequence]
        id_line = account_move_line_model.create(vals)
        return id_line

    @api.model
    def _make_transitory_move_line(self, line,
                                   computed_lines, move_id, period_id,
                                   trans_account_id, partner_id):
        account_move_line_model = self.env['account.move.line']
        analytic_account_id = False
        if line.analytic_account_id:
            if not line.journal_id.analytic_journal_id:
                raise exceptions.Warning(
                    _('No Analytic Journal !'),
                    _("You have to define an analytic journal "
                      "on the '%s' journal!")
                    % (line.template_id.journal_id.name,)
                )
            analytic_account_id = line.analytic_account_id.id
        vals = {
            'name': 'transitory',
            'move_id': move_id,
            'journal_id': line.journal_id.id,
            'period_id': period_id,
            'analytic_account_id': analytic_account_id,
            'account_id': trans_account_id,
            'date': time.strftime('%Y-%m-%d'),
            'partner_id': partner_id,
        }
        if line.move_line_type != 'cr':
            vals['credit'] = computed_lines[line.sequence]
        if line.move_line_type != 'dr':
            vals['debit'] = computed_lines[line.sequence]
        id_line = account_move_line_model.create(vals)
        return id_line

    @api.multi
    # Make it regular way via wizzard
    def triger_template_wizzard(self, vals):
        wizard = self.env.ref('account_move_template.wizard_select_template')

        buffer = ({
            'template_id': self.template_id.id,
            'partner_id': self.partner_id.id,
        })

        _logger.info('EEEEEEEEEEEEE______template_id________EEEEEEEEEEEEEE %s', buffer['template_id'])
        _logger.info('GGGGGGGGGGGGG______partner_id_________GGGGGGGGGGGGGG %s', buffer['partner_id'])

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.select.move.template',
            'name': _('Select Move Template'),
            'view_id': wizard.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy': True,
            # 'context': context
        }

