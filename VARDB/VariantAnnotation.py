# -*- coding: utf-8 -*-
"""
Created on Wed May 24 19:27:42 2017

@author: gburguener
"""


import os
import sys


from VARDB import sqldb, VARDBBase
from peewee import Model, ForeignKeyField, CharField
from VARDB.VariantAssignment import VariantAssignment



class VariantAnnotation(VARDBBase):
    assignment =  ForeignKeyField(VariantAssignment, related_name='annotations', 
                                          db_column="assignment_fk")  
    source_type = CharField(choices=["DB", "prediction", "biblio"]) 
    source = CharField()
    prop = CharField()
    value = CharField()
    description = CharField(null=True)
    
    class Meta:
        database = sqldb
        
        
if __name__ == '__main__':
    VariantAnnotation.create_table()