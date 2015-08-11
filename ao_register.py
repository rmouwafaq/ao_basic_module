# -*- coding: utf-8 -*-
import os


#====================================================================
# Directories  
CD_ODOO_ADDONS     = os.getcwd()+ '/'+"addons/" 
CD_STATIC_REPORTS  = CD_ODOO_ADDONS + "report_def/static/reports/"


#===============================================================================
# ao_modules_folder_name as a dictionnary:
#    key : is the module name agilorg
#    value : is the module folder name
#===============================================================================
ao_modules_folder_name={
                        'Report Definition':'report_def',
                        'Report Storage':'report_def_store',
                        'payroll_AgilOrg':'payroll_AgilOrg',
                        'payroll_reporting':'payroll_reporting',
                        'Financial_Reporting':'account_financial_report',
                        'Multiple Operator Telecommunication Reload Management':'mo_recharge'
                }
