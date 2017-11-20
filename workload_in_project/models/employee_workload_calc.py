# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Jesni Banu(<http://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from openerp import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

DEF_WORK_DAYS = 5
DEF_NO_OF_DAYS = 7
DEF_WORK_HR = 8


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    progress_rate = fields.Integer(string='Workload')
    maximum_rate = fields.Integer()
    users_workload_hrs = fields.Integer(string='Current Workload [hrs]')
    max_workload = fields.Integer(string='Maximum workload [hrs]')

    """
    Function takes calculates workload based on remaining time for all tasks within the deadline and maximum workload
    """
    @api.model
    def fields_view_get(self, view_id=None, view_type='kanban', toolbar=False, submenu=False):
        ret_val = super(ResUsersInherit, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        today = datetime.today().date()
        ir_values = self.env['ir.values']
        no_of_days = ir_values.get_default('project.config.settings', 'no_of_days')
        no_of_hrs = ir_values.get_default('project.config.settings', 'working_hr')

        # Look at the each user and select task within deadlines
        for user in self.search([]):
            users_workload_hrs = 0.0
            max_workload = 0.0

            if no_of_days:
                worload_boudary_date = datetime.today() + timedelta(days=no_of_days - 1)
            elif no_of_days == 0:
                user.write({'maximum_rate': 100,
                            'progress_rate': 0})
                return ret_val
            else:
                worload_boudary_date = datetime.today() + timedelta(days=DEF_NO_OF_DAYS)
                no_of_days = DEF_NO_OF_DAYS
            task_within_deadline = self.env['project.task'].search([('user_id', '=', user.id),
                                                    ('date_deadline', '>=', fields.Date.today()),
                                                    ('date_deadline', '<=', worload_boudary_date)])

            _logger.info('gggggggggggggggg______deadline_date_________ggggggggggggg %s', worload_boudary_date)


            # Sum up all the remaining workload for tasks within deadlines
            for each_task in task_within_deadline:
                remaining_hours = each_task.remaining_hours
                users_workload_hrs += abs(remaining_hours)

            # Calculate users max load based on schedule excluding leaves
            employee = self.env['hr.employee'].search([('id', '=', user.id)])

            # If there is a schedule calculate max workload based on it
            if len(employee.calendar_id) != 0:
                work_schedule = employee.calendar_id

                # Calculate max workload
                hours_in_weekday = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0 }

                work_time = work_schedule.attendance_ids

                # Write work schedule hours into dict
                for schedule_line in work_time:
                    time = schedule_line.hour_to - schedule_line.hour_from
                    hours_in_weekday[str(schedule_line.dayofweek)] += time

                # Calculate max_workload for a give period
                for day in range(no_of_days):
                    current_day = today + timedelta(days=day)
                    max_workload += hours_in_weekday[str(current_day.weekday())]

                max_workload_after_leaves = max_workload

                # Substract leaves from max_workload for a given period
                leaves = work_schedule.leave_ids
                for leave in leaves:
                    date_to = datetime.strptime(leave.date_to, '%Y-%m-%d %H:%M:%S')
                    date_from = datetime.strptime(leave.date_from, '%Y-%m-%d %H:%M:%S')
                    diff = date_to - date_from
                    if date_from >= datetime.today():
                        for day in range(diff.days + 1): # if there is a leave it is at least one day
                            current_day = date_from + timedelta(days=day)
                            if current_day < worload_boudary_date:
                                max_workload_after_leaves -= hours_in_weekday[str(current_day.weekday())]
                            else:
                                break
                max_workload = max_workload_after_leaves
            # If there is no schedule use default values
            else:
                for day in range(no_of_days):
                    current_day = today + timedelta(days=day)
                    if current_day.weekday() in range(DEF_WORK_DAYS):
                        if no_of_hrs != 0 and no_of_hrs != None:
                            max_workload += no_of_hrs
                        else:
                            max_workload += DEF_WORK_HR

            _logger.info('ttttttttttttttttt______max_workload_________ttttttttttttttt %s', max_workload)

            workload_perc = (users_workload_hrs / max_workload) * 100
            user.write({'maximum_rate': 100,
                        'progress_rate': workload_perc,
                        'users_workload_hrs': users_workload_hrs,
                        'max_workload': max_workload
                        })
        return ret_val




class ProjectSettings(models.TransientModel):
    _inherit = 'project.config.settings'

    working_hr = fields.Integer(string='Standard working Hr/day', default=DEF_WORK_HR)
    no_of_days = fields.Integer(string='No of days for calculation', default=DEF_NO_OF_DAYS)
    block_busy_users = fields.Boolean(string='Block busy users ?', default=False)

    @api.multi
    def set_block_busy_users(self):
        return self.env['ir.values'].sudo().set_default(
            'project.config.settings', 'block_busy_users', self.block_busy_users)

    @api.multi
    def set_working_hr(self):
        return self.env['ir.values'].sudo().set_default(
            'project.config.settings', 'working_hr', self.working_hr)

    @api.multi
    def set_no_of_days(self):
        return self.env['ir.values'].sudo().set_default(
            'project.config.settings', 'no_of_days', self.no_of_days)


class ProjectInherit(models.Model):
    _inherit = 'project.task'

    @api.constrains('user_id')
    def validation(self):
        ir_values = self.env['ir.values']
        block_users = ir_values.get_default('project.config.settings', 'block_busy_users')
        if block_users:
            if self.user_id.progress_rate > 80:
                raise Warning(_('%s is %s percentage Overloaded with Work') % (self.user_id.name, self.user_id.progress_rate))


class EmployeeWorkloadReport(models.TransientModel):
    _name = "wizard.workload.report"
    _description = "Employee Workload Report"

    working_hr = fields.Integer(string='Working Hr/day', required=True, default=DEF_WORK_HR)
    from_date = fields.Date(string='From Date', required=True, default=lambda *a: datetime.now().strftime('%Y-%m-%d'))
    to_date = fields.Date(string='To Date', required=True, default=datetime.today() + timedelta(days=DEF_NO_OF_DAYS))

    @api.multi
    def workload_report(self):
        data = self.read()[0]
        datas = {
            'ids': [],
            'model': 'wizard.workload.report',
            'form': data
        }
        return self.env['report'].get_action(self, 'workload_in_project.report_employee_workload', data=datas)

