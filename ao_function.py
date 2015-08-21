# -*- coding: utf-8 -*-
import collections
import csv


#===============================================================================
# function money_counting() :
# 
#===============================================================================
def money_count(montant,list_monnaie=()):
        nb_monaie=collections.OrderedDict()
        for k in xrange(len(list_monnaie)):
            nb_monaie[list_monnaie[k]]=0
        for piece in list_monnaie:
            nb_monaie[piece]=int(montant/piece)
            montant = montant - (nb_monaie[piece] * piece)
        return nb_monaie


