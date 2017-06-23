# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""

from  VARDB.VariantCollection import mysql_db
from peewee import Model, CharField, DateTimeField, TextField
import datetime
        

class ProgramRun(Model):
      
    name = CharField(null=True)
    program = CharField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    description = TextField()    
    format = CharField()
    '''
    Ouput format
    '''

    class Meta:
        database = mysql_db


if __name__ == '__main__':
    ""
        
    ProgramRun.create_table()
          
