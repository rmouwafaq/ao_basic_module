# -*- coding: utf-8 -*-
import time
import os

#===============================================================================
# Global function 
# 
#===============================================================================

def remove_any(strsource,pattern ):
    #---- remove any char in pattern
    i  = 0
    while i<= len(pattern)-1:
        strsource = strsource.replace(pattern[i],"")
        i += 1
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
        file_name = file_name + str_end
    return file_name

def create_folder(path_target):
    try:
        os.mkdir(path_target)
        return True
    except OSError:
        pass
        return True
  