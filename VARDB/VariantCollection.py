# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:02:26 2017

@author: gburguener
"""

from peewee import *
from VARDB import sqldb, VARDBBase
import datetime



class VariantCollection(VARDBBase):
    ref_organism = CharField()
    sample = CharField()
    description = CharField(null=True)    
    modified_date = DateField(default=datetime.datetime.now)

    class Meta:
        indexes = (            
            (('ref_organism', 'sample'), True),

        )
        database = sqldb 
        
        
if __name__ == '__main__':
    VariantCollection.create_table()
          
