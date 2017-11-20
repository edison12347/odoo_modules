# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, fields, api


class task(models.Model):
    _inherit = 'project.task'

    issue_ids = fields.One2many(
        'project.issue', 'task_id', string="Project Issue")
    issue_id = fields.Many2one(
        'project.issue',
        string='Main Issue',
        compute='get_issue',
        #store=True,
    )

    @api.one
    def get_issue(self):
        if len(self.issue_ids):
            self.issue_id = self.issue_ids[0]
        else:
            self.issue_id = False
