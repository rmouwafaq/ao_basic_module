# -*- coding: utf-8 -*-
import os


#====================================================================
# Directories  
CD_ODOO_ADDONS     = os.getcwd()+ '/'+"openerp/addons/" 
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
    _description = 'registry'
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
    _columns = {
                'name'          : fields.char('Designation', 128, required=True),
                'description'   : fields.text('Description'),
                #'category_id'   : fields.many2one('mor.registry.category','Category'),
                'type'          : fields.selection([('int','Nombre naturel'),
                                           ('char','Chaine de caractères'),
                                           ('date','Date'),
                                           ('datetime','Date et heure'),
                                           ('path','Lien'),
                                           ('float','Nombre décimal'),
                                           ('boolean','Boolean')],'Type', required=True),
                'value'         : fields.char('Valeur', 128),
                'default'       : fields.char('Valeur par défaut', 128, required=True),
                'parent_id'     : fields.many2one('ao.registry', 'Registre parent', select=True),
                'child_ids'     : fields.one2many('ao.registry', 'parent_id', 'Sous registres'),
                # Pour gérer l'arborescence parent-fils
                'parent_left'   :   fields.integer('Left parent', select=True),
                'parent_right'  :   fields.integer('Right parent', select=True),
            }
    _sql_constraints = [('name', 'UNIQUE (name)', 'Nom du registre dupliqué. Vous ne pouvez pas définir deux registres ayant le même nom !')]
    
    def get_childs_by_name(self, cr, uid, name, context=None, cols=None):
        '''
        Utilise l'opérateur 'child_of' pour récupérer les registres fils
        de l'utilisateur uid
        
        :param: fields: list des champs à lire 
        :return: list(dict) or list       
        '''
        domain = []
        if context is None: context = {}
        if fields is None: cols = []
        
        # Recherche l'id registre par nom
        registry_id= self.search(cr, uid, [('name','=',name)] )[0]['name']
        
        # Récupère tableau des ids des sous registres 
        domain.append(('id', 'child_of', registry_id))
        ids = self.search(cr, uid, domain, 0, None, None, context, False)
        
        # Retourne un dictionnaire de valeurs
        return self.read(cr, uid, ids, cols)    
    
    def registre_Valeur(self, code):
        self.cr.execute('select valeur from mor.registre.categorie where code=%s', (code,))
        var_valeur = self.cr.fetchone()[0]
        if var_valeur is None:
            #print 'Valeur n\'existe pas'
            return False
        else:
            return var_valeur
  
    def create_Registre(self,cr,uid, code, name, categorie, type_value, valeur, defaut):
        pool_cat = self.pool.get('mor.registre.categorie')
        categorie_id = pool_cat.get_categorie(cr,uid,categorie)
        dic_reg = {
                       'code'           : code,
                       'name'           : name,
                       'categorie_id'   : categorie_id,
                       'type'           : type_value,
                       'valeur'         : defaut,
                       'defaut'         : defaut                       
                       }
        
        return self.create(cr,uid,dic_reg)
          
    def get_set_registre(self,cr,uid,cat,code,name,defaut,type_value='char',valeur=None):
        
        id_reg = self.search(cr,uid , [('code','=',code)])
        if not id_reg:
            if valeur==None:
                valeur=defaut
            self.create_Registre(cr, uid, code, name, mor_registry, type_value, valeur, defaut)
            return defaut
        
        else:
            dic_reg = self.read(cr,uid,id_reg, ['valeur'])
            registre = dic_reg[0]
            return self.reg_value(type_value,registre['valeur'])
            
    def reg_value(self,type_value,valeur):     
        if type_value == 'int':
            return int(valeur)
        elif type_value == 'float':
            return float(valeur)
        else:
            return valeur 
        
        
    def delete_Registre(self,cr,uid,code):
        id_reg = self.search(cr,uid , [('code','=',code)])   
        if id_reg:  
            self.unlink(cr, uid, id_reg)  
        return True
    
    def exist_Registre_Code(self,cr,uid,code):
        id_reg = self.search(cr,uid , [('code','=',code)])
        self.fields_get(cr, uid)
        if id_reg:
            return True
        else:
            return False 


