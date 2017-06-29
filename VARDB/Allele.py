# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:43:43 2017

@author: gburguener
"""



from peewee import ForeignKeyField,  CharField,  DeferredRelation
from VARDB.Variant import Variant
from VARDB import sqldb, VARDBBase



DeferredEffect = DeferredRelation()

class Allele(VARDBBase):
    
    variant =  ForeignKeyField(Variant, related_name='alleles', 
                                          db_column="variant_fk")  
    alt = CharField()
    main_effect =ForeignKeyField(DeferredEffect,  db_column="main_effect_fk",null=True)
  
    
    class Meta:
        database = sqldb
        indexes = (            
            (('variant','alt'), True),

        )
        
if __name__ == '__main__':
    Allele.create_table()