# -*- coding: utf-8 -*-
"""
Created on Wed May 24 19:27:42 2017

@author: gburguener
"""


import os
import sys


from VARDB import mysql_db
from peewee import Model, ForeignKeyField, CharField
from VARDB.VariantAssignment import VariantAssignment



class VariantAnnotation(Model):
    assignment =  ForeignKeyField(VariantAssignment, related_name='annotations', 
                                          db_column="assignment_fk")  
    source_type = CharField() #DB, prediccion, bibliografia
    source = CharField()
    prop = CharField()
    value = CharField()
    description = CharField()
    
    class Meta:
        database = mysql_db
        
        
if __name__ == '__main__':
    VariantAnnotation.create_table()