# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""

from  VARDB.VariantCollection import mysql_db
from peewee import Model, CharField, DateTimeField, TextField, ForeignKeyField
from VARDB.ProgramRun import ProgramRun
        

class ProgramParameter(Model):
    
    
    run =  ForeignKeyField(ProgramRun, related_name='parameters', 
                                          db_column="run_fk") 
    
    name = CharField()    
    value = CharField()
    

    class Meta:
        database = mysql_db


          
