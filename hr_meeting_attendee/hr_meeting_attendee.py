from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class meeting_attendee(models.Model):

    """ Model for Calendar Event """
    _name = 'calendar.event'
    _inherit = 'calendar.event'
    _description = "Parse and adds attendees to the partner_ids in meetings"

    def create(self, cr, uid, vals, context=None):

        if context is None:
            context = {}

        self._set_date(cr, uid, vals, id=False, context=context)
        if not 'user_id' in vals:  # Else bug with quick_create when we are filter on an other user
            vals['user_id'] = uid
        # Get id of the apdplicant and user NEW API

        applicant_id = context.get('active_id',False)
        applicant = self.pool.get('hr.applicant').browse(cr, uid, applicant_id)
        applicant_creator = applicant.partner_id.id
        applicant_creator_id = applicant.create_uid.id

        user = self.pool.get('res.users').browse(cr, uid, applicant_creator_id)
        user_partner_id = user.partner_id.id

        partner_ids_list = []
        partner_ids_list.append([4, user_partner_id])
        partner_ids_list.append([4, applicant_creator])
        vals['partner_ids'] = partner_ids_list

        _logger.info('AAAAAAAAAAAAAAAAAAAa______applicant_creator_________AAAAAAAAAAAAAAAAAaa %s', applicant_creator)
        _logger.info('UUUUUUUUUUUUUUUUUUUUU______user_partner_id_________UUUUUUUUUUUUUUUUUUUUUU %s', user_partner_id)

        res = super(meeting_attendee, self).create(cr, uid, vals, context=context)

        final_date = self._get_recurrency_end_date(cr, uid, res, context=context)
        self.write(cr, uid, [res], {'final_date': final_date}, context=context)
        self.create_attendees(cr, uid, [res], context=context)



        return res

       
        
        # Get id of the applicant and user NEW API

        # applicant_id = self._context.get('active_id',False)
        # applicant = self.env['hr.applicant'].search([('id','=',applicant_id)])
        # applicant_creator = applicant.create_uid.id

        # user = self.env['res.users'].search([('id','=',applicant_creator)])
        # user_partner_id = user.partner_id.id

        # Get id of the applicant and user OLD API

        # applicant_id = context.get('active_id',False)
        # applicant = self.pool.get('hr.applicant').browse(cr, uid, applicant_id)
        # applicant_creator = applicant.partner_id.id
        # applicant_creator_id = applicant.create_uid.id
        

        # user = self.pool.get('res.users').browse(cr, uid, applicant_creator_id)
        # user_partner_id = user.partner_id.id

        # partner_ids_list = []
        # partner_ids_list.append([4, user_partner_id])
        # partner_ids_list.append([4, applicant_creator])
        # vals['partner_ids'] = partner_ids_list


        # _logger.info('AAAAAAAAAAAAAAAAAAAa______applicant_creator_________AAAAAAAAAAAAAAAAAaa %s', applicant_creator)
        # _logger.info('UUUUUUUUUUUUUUUUUUUUU______user_partner_id_________UUUUUUUUUUUUUUUUUUUUUU %s', user_partner_id)
