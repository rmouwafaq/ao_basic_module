import os
from math import floor
from openerp.addons.ao_basic_module.ao_register import CD_STATIC_REPORTS,CD_ODOO_ADDONS


class amount_to_letter():
    def __init__(self,mont,devise,cent_devise,genre):
        self.mont=mont
        self.devise=devise
        self.cent_devise=cent_devise
        self.lettre=" "
        
        self.tconu=["UN","DEUX","TROIS","QUATRE","CINQ","SIX","SEPT","HUIT","NEUF"]
        
        if(genre==1):self.tconu[0]="UNE"
        self.tcondv=["ONZE","DOUZE","TREIZE","QUATORZE","QUINZE","SEIZE","DIX SEPT","DIX HUIT","DIX NEUF"]
        self.tcond=["DIX","VINGT","TRENTE","QUARANTE","CINQUANTE","SOIXANTE","SOIXANTE DIX","QUATRE VINGT","QUATRE VINGT DIX"]
        
        if(mont<=0):
            return None
        self.mont_traduit()
        return None
    
    def mont_traduit(self):
        tdec=self.mont_decompose(self.mont)
        traduc=[" "," "," "," "," "]
        de=""
        for i in xrange(4):
            k=self.mont_convertion(tdec[i])
            traduc[i]=self.chch

        if(tdec[0]>=1 ):
            traduc[4]=traduc[0]+self.cent_devise
        traduc[4]=traduc[1]+self.devise+traduc[4]
        
        if(tdec[2]==1):
            traduc[4]=" MILLE "+traduc[4]
        
        if(tdec[2]>1):
            traduc[4]=traduc[2]+" MILLE "+traduc[4]
        
        if(traduc[4].strip()==""):
            de="DE "
        else:
            de=""
        if(tdec[3]==1):
            traduc[4]="UN MILLION "+de+traduc[4]
        if(tdec[3]>1):
            traduc[4]=traduc[3]+"MILLIONS "+de+traduc[4]
        self.lettre=traduc[4]
        
    def mont_convertion(self,mont):
        self.chch=" "
        self.nbc=0
        self.nbd=0
        self.nbu=0
        self.nbc=mont//100
        self.nbd=(mont//10)-((self.nbc*100)//10) 
        self.nbu=(mont-(self.nbc*100))-self.nbd*10
        
        
        if(self.nbc+self.nbd+self.nbu==0):
            return ""
        if(self.nbc==0):
            self.montconv1()
            return None
        if(self.nbc==1):
            self.chch=self.chch+"CENT "
            self.montconv1()
            return None
        if(self.nbc>1 and (self.nbd+self.nbu==0)):
            self.chch=self.chch+self.tconu[self.nbc-1]+" CENTS "
            return ""
        self.chch=self.chch+self.tconu[self.nbc-1]+" CENT "
        
        if(self.nbu!=0):
            self.chch=self.chch+self.tcond[self.nbd-1]+" "+self.tconu[self.nbu-1]+" "
        else:
            self.chch=self.chch+self.tcond[self.nbd-1]+" "
        return ""
        
    def montconv1(self):
        if(self.nbd!=1):
            self.montconv2()
            return None
        if(self.nbu==0):
            self.chch=self.chch+"DIX"
        else:
            self.chch=self.chch+self.tcondv[self.nbu-1]
        return None
    
    def montconv2(self):
        if(self.nbd!=7 and self.nbd!=9):
            self.montconv3()
            return None
        if(self.nbu==0):
            self.chch=self.chch+self.tcond[self.nbd-1]+" "
            return None
        if(self.nbu==1):
            self.chch=self.chch+self.tcond[self.nbd-2]+" ET "+self.tcondv[self.nbu-1]+" "
        if(self.nbu!=1):
            self.chch=self.chch+self.tcond[self.nbd-2]+" "+self.tcondv[self.nbu-1]+" "
        return None
    
    def montconv3(self):
        if(self.nbd==0):
            if(self.nbu!=0):
                self.chch=self.chch+self.tconu[self.nbu-1]+" "
                return None
        if(self.nbd==8 and self.nbu==0):
            self.chch=self.chch+self.tcond[self.nbd-1]+"S "
            return None
        if(self.nbu==1):
            self.chch=self.chch+self.tcond[self.nbd-1]+" ET "+self.tconu[self.nbu-1]+" "
            return None
        if(self.nbu==1):
            self.chch=self.chch+" "+self.tcond[self.nbd-1]+" ET "+self.tconu[self.nbu-1]
        if(self.nbu!=0):
            self.chch=self.chch+self.tcond[self.nbd-1]+" "+self.tconu[self.nbu-1]+" "
        else:
            self.chch=self.chch+self.tcond[self.nbd-1]+" "
        return None

    def mont_decompose(self,mont):
        tpas=[0,0,0,0]
        if(int(floor(mont))!=mont):
            tpas[0]=int((mont*100)-(int(floor(mont))*100))
        m=1000000
        
        for i in xrange(3,0,-1):
            tpas[i]=int(floor(mont/m))
            mont=mont-tpas[i]*m
            m=m/1000
        return tpas

    def get_lettrer_amount(self):
        return self.lettre
    
#===============================================================================
# 
#===============================================================================
class base_report():
    def __init__(self,report_name,module_name,json_file_name,template_file_name):
        self.attributes = {}
        self.attributes['path_json_file'] = CD_STATIC_REPORTS +module_name+"/"+report_name+"/JSON/"+json_file_name   
        self.attributes['html_template'] =  None
        self.attributes['path_template_source'] =  CD_ODOO_ADDONS + module_name + "/templates/"
        self.attributes['file_template'] =  template_file_name + '.html'
        self.attributes['path_name_output'] = CD_STATIC_REPORTS + module_name+"/"+report_name+"/HTML/"
        
    def get_report_attributes(self):
        return self.attributes
        

class model_key(object):
    
    def __init__(self,key_name,desc):
        self.vars = key_name.split(',')
        self.key_name  = key_name
        self.var_value = {}
        self.var_type  = {}
        
        for var in self.vars:
            if desc.has_key(var):
                self.var_type[var] = desc[var]['type']
                
        
    def _key(self):
        return self.key_name
    
    def get_key_value(self,obj_value):
        type_var = True 
        self.var_value = {}
        if type(obj_value) is dict:
            type_var = False
        
        for var in self.vars:
            self.var_value[var] =  ''
            if type_var :
                if self.var_type[var] == 'many2one':
                    record = getattr(obj_value, var)
                    self.var_value[var] = str(getattr(record, 'name'))
                else:
                    self.var_value[var] = str(getattr(obj_value, var))
            else:
                if obj_value.has_key(var):
                    if self.var_type[var] == 'many2one':
                        self.var_value[var] = obj_value[var][1]
                    else:
                        self.var_value[var] = obj_value[var]
        return self.var_value 
    
    
    def val_to_string(self,obj_value,sep = '_'):
        self.var_value = self.get_key_value(obj_value)
        value = ''
        sep_var   = ''
        for var in self.vars:
            if self.var_value[var] != '':  
                value = value + sep_var + str(self.var_value[var]).replace(' ',sep)
                sep_var = sep
        return value
        