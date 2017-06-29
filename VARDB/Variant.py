# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""

import datetime
from peewee import  IntegerField, CharField,  DateTimeField

from VARDB import sqldb, VARDBBase

      
class Variant(VARDBBase):
    pos = IntegerField()
    gene = CharField(null=True)
    gene_pos = IntegerField(null=True)
    contig = CharField()
    description = CharField(null=True)    
    ref_organism = CharField()
    ref = CharField()

    modified_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (            
            (('ref_organism','contig', 'pos',"ref"), True),

        )
        database = sqldb


if __name__ == '__main__':
    ""
        
    Variant.create_table()
          
