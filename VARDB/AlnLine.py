# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""


from VARDB.Alignment import Alignment
from VARDB import sqldb
from peewee import Model, ForeignKeyField, IntegerField, TextField, CharField
        

class AlnLine(Model):
    
    alignment = ForeignKeyField(Alignment, related_name='lines',
                                          db_column="alignment_fk") 
  
    start = IntegerField(null=True)
    end = IntegerField(null=True)    
    seq = TextField(null=True)
    name = CharField()
    
    class Meta:
        database = sqldb


if __name__ == '__main__':
    ""
        
    AlnLine.create_table()
          
