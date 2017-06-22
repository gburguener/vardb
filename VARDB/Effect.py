# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:45:46 2017

@author: gburguener
"""

import os
import sys
from peewee import Model, ForeignKeyField, CharField, BooleanField, IntegerField
from VARDB.Variant import Variant
from VARDB import sqldb, VARDBBase





class Effect(VARDBBase):
    from VARDB.Allele import Allele
    allele =  ForeignKeyField(Allele, related_name='effects', 
                                          db_column="allele_fk")  
    
    transcript = CharField(null=True)
    variant_type = CharField() #SO term, inherited from SO variant type.
    reported = BooleanField(default=False)
    predicted_impact = CharField(null=True) 
    aa_ref = CharField(null=True)
    aa_pos = IntegerField(null=True)
    aa_alt = CharField(null=True) 
    
    class Meta:
        database = sqldb
        
        
if __name__ == '__main__':
    Effect.create_table()