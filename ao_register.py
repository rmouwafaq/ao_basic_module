# -*- coding: utf-8 -*-
import os
from openerp.modules import module

#====================================================================
# Directories  
CD_ODOO_ADDONS     = os.getcwd()+ '/'+"addons/" 
CD_REPORT_DEF      = module.get_module_path('report_def')
CD_STATIC_REPORTS  = CD_REPORT_DEF + "/static/reports/"
CD_AO_FIN_REPORT   = module.get_module_path('account_financial_report')+ "/"


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

#-*- coding: utf-8 -*-
from openerp.osv import fields
from openerp.osv import osv


class ao_registry(osv.osv):
#     @note: Pour plus de details sur les registres
#     @contact: http://msdn.microsoft.com/en-us/library/windows/desktop/ms724946(v=vs.85).aspx
#     @http://www.speedtools.org/fr/registry-structure.php
#     '''
#     
#     'name'          : Nom du registre
#     'description'   : Description
#     'category_id'   : Nom de la catégorie associée au registre
#     'type'          : Type de valeur stcokée, char, float, int...
#     'value'         : Valeur du registre
#     'default'       : Valeur par défaut
#     'parent_id'     : Registre parent
#     'child_ids'     : Sous registres 
#     'parent_left'   : 
#     'parent_right'  :
#     Pour plus d'informations sur les champs parent_left, parent_right 
#     https://www.odoo.com/forum/help-1/question/what-is-the-meaning-of-parent-left-and-parent-right-domain-operator-25221
#     '''
    _name = 'ao.registry'
    _parent_order = 'name'
    _columns = {
                'name'          : fields.char('Key', 128, required=True),
                'module_id'     : fields.many2one('ir.module.module', 'Module'),
                'type'          : fields.selection([('int','int'),
                                           ('char','char'),
                                           ('text','text'),
                                           ('html','html'),
                                           ('date','date'),
                                           ('datetime','datetime'),
                                           ('selection','selection'),
                                           ('list','list'),
                                           ('dictionary','dictionary'),
                                           ('binary','binary'),
                                           ('path','path'),
                                           ('float','float'),
                                           ('boolean','boolean')],'Type', required=True),
                'value'         : fields.text('Valeur'),
                'default'       : fields.text('Valeur par défaut',required=True),
                'parent_id'     : fields.many2one('ao.registry', 'Registre parent', select=True),
                'description'   : fields.text('Description'),
            }
    _sql_constraints = [('name', 'UNIQUE (name)', 'Nom du registre dupliqué. Vous ne pouvez pas définir deux registres ayant le même nom !')]
    
    def get_param(self,cr,uid,name,context=None):
        
        id_reg = self.search(cr,uid , [('name','=',name)])
        if not id_reg:
            print 'parameter not found !!!'
        
        else:
            param = self.browse(cr,uid,id_reg)
            if param.value:
                value = param.value
            else :
                value = param.default
            return self.cast_value(param.type,value)
        
    def set_param(self,cr,uid,name,valeur,context=None):
        
        id_reg = self.search(cr,uid , [('name','=',name)])
        if not id_reg:
            print 'parameter not found !!!'
        else:
            self.write(cr,uid,id_reg,{'value':valeur})
            param = self.browse(cr,uid,id_reg)
            if param.value:
                value = param.value
            else :
                value = param.default
            return self.cast_value(param.type,value)
            
    def cast_value(self,type_value,valeur):     
        if type_value == 'int':
            return int(valeur)
        elif type_value == 'float':
            return float(valeur)
        elif type_value == 'char' or type_value == 'text':
            return str(valeur)
        else:
            return valeur 
        
