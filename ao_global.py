# -*- coding: utf-8 -*-

#===============================================================================
# Global function 
# 
#===============================================================================


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
  