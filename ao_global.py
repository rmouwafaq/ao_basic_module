# -*- coding: utf-8 -*-
import time
import os


import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

#===============================================================================
# Global function 
# 
#===============================================================================


def str_mid(vstr,startpos=0,endpos=0):
    if endpos == 0 :
        endpos = len(vstr)-1
    return vstr[startpos:endpos]

def remove_any(strsource,pattern ):
    #---- remove any char in pattern
    if strsource:
        for char in strsource:
            if char in pattern:
                strsource = strsource.replace(char,'')
    return strsource
    

def stringtofile(strfile,filename):
    ofi = open(filename, 'w')
    ofi.write(strfile)
    ofi.close

    
def sql_type(vals):
    tvals = list()
    for field in vals:
        mytype = type(vals[field])
        myval = sql_format(vals[field],mytype)
        tvals.append(myval)
    return tvals

def sql_str(vals):
    tvals = list()
    for field in vals:
        mytype = type(vals[field])
        myval = sql_str_format(mytype)
        tvals.append(myval)
    return tvals


def sqlformat_byte(valeur):
    if valeur.upper() == "false" : 
        valeur = "0"
    elif valeur.upper() == "true" :
        valeur ="1"
    return valeur 

def sqlformat_number(valeur):
    return valeur

def sqlformat_date(valeur):
    return str(valeur) 

def sqlformat_default(valeur):
    valeur = valeur.replace("'", "") 
    return valeur

def sql_format(valeur,typechamp):
       
    takeaction = {
    bool: sqlformat_byte,
    int:sqlformat_number,
    float:sqlformat_number,
    long:sqlformat_number,
    datetime.datetime :sqlformat_date }
    valformat = takeaction.get(typechamp,sqlformat_default)(valeur)
    
    return valformat

def sql_str_format(typechamp):
       
    takeaction = {
    bool: '%s',
    int:'%s',
    float:'%s',
    long:'%s',
    datetime.datetime :'%s',
    datetime.date :'%s'
     }
    str_format = takeaction.get(typechamp,'%s') 
    
    return str_format

'''
     retourne une liste des id d'une liste forunie d'objets records
'''
def records_to_list(object_ids):
    rec_list = []
    for rec in object_ids:
        rec_list.append(rec.id)
    return rec_list 


'''
    transforme les élements une liste en un dictionnaire
'''
def list_to_dict(list_elements):
    dict_elements ={}
    for key in list_elements:
        dict_elements[key]=""
    return dict_elements    

def end_file(file_name,str_end):
    if not file_name.endswith(str_end):
        return file_name + str_end
    else:
        return file_name

def create_folder(path_target):
    try:
        os.mkdir(path_target)
        return True
    except OSError:
        pass
        return True

def string_to_value(value,type = 'int'):
    n_value = 0
    if value:
        if isinstance(value, str) or isinstance(value, unicode):
            value = ''.join(value.split()).replace(',',".").replace('%','')
        try: 
           if type == 'float':
               n_value = float(value)
           elif type == 'int':
               n_value = int(float(value))
           else:
               n_value = double(value)
        except ValueError:
           n_value = 0

    return n_value
 
def is_number(s):
    if s:
        if isinstance(s,str):
            s = ''.join(s.split()).replace(',',".").replace('%','') 
        try:
            float(s)
            return True
        except ValueError:
            return False
    return False

def ao_format(pos,dec,sep):
        pp = pos + dec 
        if len(sep)>0:
            return '{:'+ sep + '>' + str(pp) + ',.'+str(dec)+'f}'
        else: 
            return '{:>' + str(pp) + ',.'+str(dec)+'f}'


REF_FORMAT_TD = {
              'text' : '{}',
              '' : '{}',  
              'DJMA': '{}',
              'JMA': '{}',
              'AMJ': '{}', 
              'E2':  '{:>2.0f}',
              'E3':  '{:>3.0f}',
              'E4':  '{:>4.0f}',
              'E5':  '{:>5.0f}',
              'E6':  '{:>6.0f}',
              'E7':  '{:>7.0f}',
              'E8':  '{:>8.0f}',
              'E9':  '{:>9,.0f}',
              'F10': '{:>10,.2f}',
              'F11': '{:>11,.2f}',
              'F12': '{:>12,.2f}',
              'F13': '{:>13,.2f}',
              'F14': '{:>14,.2f}',
              'F15': '{:>15,.2f}',
              }


FORMAT_FIN_REPORT = {
                      'E2':  {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'E3':  {'format':'E3','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'E4':  {'format':'E4','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'E5':  {'format':'E5','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'E6':  {'format':'E6','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'E7':  {'format':'E7','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'E8':  {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'E9':  {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'F10': {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'F11': {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'F12': {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'F13': {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'F14': {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      'F15': {'format':'E2','sep':True,'disp_zero':True,'align':True,'ref_format':REF_FORMAT_TD},
                      }


def ao_format_value(cell_format,amount, ao_format=True):
    value = REF_FORMAT_TD[cell_format].format(amount)
    if not ao_format:
       value = value.replace(",","").replace(" ","")
    else:
        value = value.replace(","," ")
        if amount == 0:
            value = ''
    return value

def ao_decimal_format(value,attributes):
    if attributes['ref_format'].has_key(attributes['format']):
        str_form = ref_form[attributes['format']]
    else:
        str_form = attributes['ref_format']['F13']
    fmt = mystr.format(value)
    if attributes['sep']:
        fmt = fmt.replace(","," ")
    else:
        fmt = fmt.replace(",","")
    if not attributes['align']:
        fmt = fmt.replace(" ","")
    
    if value == 0:
        if attributes['disp_zero']:
            fmt = ''
    return fmt


def ao_date_format(udate,date_format):
    strdate  = remove_any(udate,"./-")
    if strdate:
        if len(strdate)==8:
            if date_format == 'JMA':
                return strdate[:2] + "-" + strdate[2:4] + "-" + strdate[-4:]
            elif date_format == 'AMJ':
                return strdate[-4:] + '-' + strdate[2:4] + "-" + strdate[:2]
            else:
                print date_format,' format date inconnu'
    return udate
