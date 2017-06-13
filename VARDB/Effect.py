# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:45:46 2017

@author: gburguener
"""

import os
import sys
from peewee import Model, ForeignKeyField, CharField, BooleanField, IntegerField
from VARDB.Variant import Variant
from VARDB import mysql_db
from VARDB.Allele import Allele




class Effect(Model):
    allele =  ForeignKeyField(Allele, related_name='effects', 
                                          db_column="allele_fk")  
    
    transcript = CharField()
    variant_type = CharField() #SO term, inherited from SO variant type.
    reported = BooleanField()
    predicted_impact = CharField() 
    aa_ref = CharField()
    aa_pos = IntegerField()
    aa_alt = CharField() 
    
    class Meta:
        database = mysql_db
        
        
if __name__ == '__main__':
    Effect.create_table()