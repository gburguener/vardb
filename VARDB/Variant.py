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
from VARDB import mysql_db



        

class Variant(Model):
    pos = IntegerField()
    gene = CharField()
    gene_pos = IntegerField()
    contig = CharField()
    description = CharField()    
    ref_organism = CharField()
    ref = CharField()

    modified_date = DateField()

    class Meta:
        database = mysql_db


if __name__ == '__main__':
    ""
        
    Variant.create_table()
          
