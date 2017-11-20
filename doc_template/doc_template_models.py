# -*- coding: utf-8 -*-
"""
Accounting Documents template

"""

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import datetime

import time
import logging

class provision_of_production_services_Act(models.Model):

    _name = 'document.template.production_services_act'
    _inherit = 'document.template'
    _description = 'The Act on the provision of production services'

    name = fields.Char('Document Name')
class reconciliation_Act(models.Model):

    _name = 'document.template.reconciliation_act'
    _description = 'Reconciliation Act'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class fixed_assets_commissioning(models.Model):

    _name = 'document.template.fixed_assets_commissioning'
    _description = 'Commissioning of the Fixed assets'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class employees_bank_cards_information(models.Model):

    _name = 'document.template.employees_bank_cards_information'
    _description = 'Entering information about bank cards of employees'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class regulated_reports_unloading(models.Model):
    _name = 'document.template.regulated_reports_unloading'
    _description = 'Unloading of regulated reports'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class amortization_calculation_dev(models.Model):
    _name = 'document.template.amortization_calculation_dev'
    _description = 'Development for calculation of amortization'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class fixed_assets_dev(models.Model):
    _name = 'document.template.fixed_assets_dev'
    _description = 'Development of the Fixed assets'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class attorney_power(models.Model):
    _name = 'document.template.attorney_power'
    _description = 'Power of Attorney'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class pers_income_tax_exemption_app(models.Model):
    _name = 'document.template.pers_income_tax_exemption_app'
    _description = 'Application for the application of the personal income tax exemption'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class work_in_progress_inventory(models.Model):
    _name = 'document.template.work_in_progress_inventory'
    _description = 'Inventory of work in progress'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class settlements_with_counterparties_inventory(models.Model):
    _name = 'document.template.settlements_with_counterparties_inventory'
    _description = 'Inventory of settlements with counterparties'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class fixed_assets_index(models.Model):
    _name = 'document.template.fixed_assets_index'
    _description = 'Indexing of the Fixed Assets'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class business_trips(models.Model):
    _name = 'document.template.business_trips'
    _description = 'Business trips'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class register_entries_adjustment(models.Model):
    _name = 'document.template.register_entries_adjustment'
    _description = 'Adjustment of register entries'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class expected_confirmed_vat_corrections(models.Model):
    _name = 'document.template.expected_confirmed_vat_corrections'
    _description = 'Correction of expected and confirmed VAT'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class standard_balances_adjustment(models.Model):
    _name = 'document.template.standard_balances_adjustment'
    _description = 'Adjustment of balances due to the entry into force of the GCC standards as of 01.04.2011'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class modernization(models.Model):
    _name = 'document.template.modernization'
    _description = 'Modernization'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class fixed_assets_repairs_modernization(models.Model):
    _name = 'document.template.fixed_assets_repairs_modernization'
    _description = 'Modernization and repair of Fixed Assets'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class tax_invoice(models.Model):
    _name = 'document.template.tax_invoice'
    _description = 'Tax Invoice'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class income_tax_expense_rationing(models.Model):
    _name = 'document.template.income_tax_expense_rationing'
    _description = 'Rationing of income tax expense'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class reflecting_mutual_settlements(models.Model):
    _name = 'document.template.reflecting_mutual_settlements'
    _description = 'Reflecting mutual settlements with counterparties in 1-DF'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class sales_commissioner_report(models.Model):
    _name = 'document.template.sales_commissioner_report'
    _description = 'Sales commissioners report'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class sales_agent_report(models.Model):
    _name = 'document.template.sales_agent_report'
    _description = 'Report to the sales agent'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class retail_sales_report(models.Model):
    _name = 'document.template.retail_sales_report'
    _description = 'Retail Sales Report'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class shift_production_report(models.Model):
    _name = 'document.template.shift_production_report'
    _description = 'Production report per shift'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class transmission(models.Model):
    _name = 'document.template.transmission'
    _description = 'Transmission of NMA'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class equipment_installation_transfer(models.Model):
    _name = 'document.template.equipment_installation_transfer'
    _description = 'Transfer of equipment to the installation'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class fixed_assets_transfer(models.Model):
    _name = 'document.template.fixed_assets_transfer'
    _description = 'Transferring the Fixed Assets'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class goods_transfer(models.Model):
    _name = 'document.template.goods_transfer'
    _description = 'Transfer of goods'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class revaluation_goods_retail(models.Model):
    _name = 'document.template.revaluation_goods_retail'
    _description = 'Revaluation of goods in retail'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class recalculation_proportional_vat(models.Model):
    _name = 'document.template.recalculation_proportional_vat'
    _description = 'Recalculation of proportional VAT on goods and fixed assets'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class payment_order_receipt_funds(models.Model):
    _name = 'document.template.payment_order_receipt_funds'
    _description = 'Payment order for the receipt of funds'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class payment_order_debiting_funds(models.Model):
    _name = 'document.template.payment_order_debiting_funds'
    _description = 'Payment order for debiting funds'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class fixed_assets_preparing_transfer(models.Model):
    _name = 'document.template.fixed_assets_preparing_transfer'
    _description = 'Preparing to transfer the fixed assets'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class processing_receip(models.Model):
    _name = 'document.template.processing_receip'
    _description = 'Receipt from processing'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class appendix_1_tax_invoice(models.Model):
    _name = 'document.template.appendix_1_tax_invoice'
    _description = 'Appendix 1 to the tax invoice'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class calculation_coefficients_completing_appendix(models.Model):
    _name = 'document.template.calculation_coefficients_completing_appendix'
    _description = 'Calculation of the coefficients for completing the Appendix'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class appendix_2_tax_invoice(models.Model):
    _name = 'document.template.appendix_2_tax_invoice'
    _description = 'Appendix 2 to the tax invoice'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class calculation_income_tax(models.Model):
    _name = 'document.template.calculation_income_tax'
    _description = 'Calculation of income tax'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class implementation_services_processing(models.Model):
    _name = 'document.template.implementation_services_processing'
    _description = 'Implementation of services for processing'
    _inherit = 'document.template'

    name = fields.Char('Document Name')


class registration_advances_accounting(models.Model):
    _name = 'document.template.registration_advances_accounting'
    _description = 'Registration of advances in tax accounting'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class registration_incoming_document(models.Model):
    _name = 'document.template.registration_incoming_document'
    _description = 'Registration of the incoming tax document'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class registration_cost_acquisition_proportionally_subject_vat(models.Model):
    _name = 'document.template.registration_cost_acquisition_proportionally_subject_vat'
    _description = 'Registration of the cost of acquisition of the fixed assets, proportionally subject to VAT'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class regulated_reports(models.Model):
    _name = 'document.template.regulated_reports'
    _description = 'Regulated report'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class income_statement(models.Model):
    _name = 'document.template.income_statement'
    _description = 'Income Statement'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class requirement_waybill(models.Model):
    _name = 'document.template.requirement_waybill'
    _description = 'Requirement-waybill'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class installation_warranty_terms(models.Model):
    _name = 'document.template.installation_warranty_terms'
    _description = 'Installation of warranty terms (tax accounting)'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class coefficient_proportional_allocation_vat_credit_setting(models.Model):
    _name = 'document.template.coefficient_proportional_allocation_vat_credit_setting'
    _description = 'Setting the coefficient of proportional allocation of VAT on credit'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class order_units_close_accounts_setting(models.Model):
    _name = 'document.template.order_units_close_accounts_setting'
    _description = 'Setting the order of units to close accounts'
    _inherit = 'document.template'

    name = fields.Char('Document Name')

class email_document(models.Model):
    _name = 'document.template.email_document'
    _description = 'Email'
    _inherit = 'document.template'

    name = fields.Char('Document Name')
