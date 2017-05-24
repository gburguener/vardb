# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""

import os
import sys
from peewee import *

sys.path.append("/home/gburguener/Documentos/Academico/WORK_UBA/Pipelines/vardb/")

from  VARDB.VariantCollection import *
        

class Variant(Model):
    variant_collection =  ForeignKeyField(VariantCollection, related_name='variants', 
                                          db_column="variant_collection_fk") 
  
    pos = IntegerField()
    gene = CharField()
    gene_pos = IntegerField()
    contig = CharField()
    description = CharField()
    modified_date = DateField()
    ref = CharField()
    genotype = CharField()
    genotype_qual = FloatField()

    class Meta:
        database = mysql_db


if __name__ == '__main__':
    ""
        
    Variant.create_table()
          
