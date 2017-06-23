# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""

import os
import sys
from peewee import Model, ForeignKeyField, IntegerField, CharField, DateField,\
    FloatField
from VARDB.VariantCollection import VariantCollection
from VARDB import sqldb, VARDBBase
import datetime



        

class Variant(VARDBBase):
    pos = IntegerField()
    gene = CharField(null=True)
    gene_pos = IntegerField(null=True)
    contig = CharField()
    description = CharField(null=True)    
    ref_organism = CharField()
    ref = CharField()

    modified_date = DateField(default=datetime.datetime.now)

    class Meta:
        indexes = (            
            (('ref_organism','contig', 'pos'), True),

        )
        database = sqldb


if __name__ == '__main__':
    ""
        
    Variant.create_table()
          
